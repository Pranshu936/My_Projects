import cv2
import numpy as np

# Paths to the configuration, weights, and classes files for YOLOv3 model
config_path = 'd:/python/object_detection/yolov3.cfg'
weights_path = 'd:/python/object_detection/yolov3.weights'
classes_path = 'd:/python/object_detection/yolov3.txt'

# Function to get output layer names from the YOLO model
def get_output_layers(net):
    layer_names = net.getLayerNames()  # Get names of all layers in the network
    # Get the output layers by finding unconnected layers, used for getting final detections
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    return output_layers

# Function to draw predictions (bounding boxes, labels, and confidence scores) on the image
def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])  # Get the class label for the detected object
    color = COLORS[class_id]  # Choose a color for the bounding box based on the class
    # Draw the bounding box
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    # Put the label and confidence score on the top-left corner of the bounding box
    cv2.putText(img, f"{label}: {confidence:.2f}", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Read class names from file and store them in a list
with open(classes_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Generate random colors for each class label for drawing bounding boxes
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# Load the YOLO model with the specified weights and config file
net = cv2.dnn.readNet(weights_path, config_path)

# Ask user for input method: use an image file or the webcam
choice = input("Enter 'image' to use an image file or 'webcam' to use the webcam: ").strip().lower()

# Function to process each frame (either from an image or webcam)
def process_frame(frame):
    # Get the dimensions of the frame (Height and Width)
    Height, Width = frame.shape[:2]
    scale = 0.00392  # YOLO's scaling factor for normalization

    # Create a blob from the input frame, resize to 416x416 for YOLO, and normalize
    blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)  # Set the blob as the input to the network

    # Forward pass through YOLO to get predictions from output layers
    outs = net.forward(get_output_layers(net))

    # Initialize lists to hold class IDs, confidences, and bounding boxes for detected objects
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5  # Minimum confidence threshold for filtering weak detections
    nms_threshold = 0.4   # Non-maximum suppression threshold for removing redundant boxes

    # Process each output from YOLO
    for out in outs:
        for detection in out:
            scores = detection[5:]  # Scores for each class
            class_id = np.argmax(scores)  # Get the class with the highest score
            confidence = scores[class_id]  # Get the highest score as confidence
            if confidence > conf_threshold:  # Only keep detections above confidence threshold
                # Calculate bounding box coordinates based on detection output
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                # Store detection results
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Apply non-maximum suppression to reduce overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # Draw bounding boxes for final detections
    if len(indices) > 0:
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box
            draw_prediction(frame, class_ids[i], confidences[i], x, y, x + w, y + h)

    return frame

# If user chose to use an image file for detection
if choice == 'image':
    image_path = input("Enter the path to the image file: ").strip()
    image = cv2.imread(image_path)  # Read the image
    if image is None:
        print(f"Error: Could not read image from {image_path}. Please check the file path.")
    else:
        processed_image = process_frame(image)  # Process the image for object detection
        cv2.imshow("Object Detection - Image", processed_image)  # Show the processed image
        cv2.imwrite("object-detection-output.jpg", processed_image)  # Save the output image
        cv2.waitKey(0)  # Wait for key press to close window
        cv2.destroyAllWindows()  # Close all OpenCV windows

# If user chose to use the webcam for real-time detection
elif choice == 'webcam':
    cap = cv2.VideoCapture(0)  # Open the default webcam (ID 0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        while True:
            ret, frame = cap.read()  # Capture a frame from the webcam
            if not ret:
                print("Error: Could not read frame from webcam.")
                break
            processed_frame = process_frame(frame)  # Process the frame for object detection
            cv2.imshow("Object Detection - Webcam", processed_frame)  # Show the processed frame
            key = cv2.waitKey(1) & 0xFF  # Wait for key press
            if key == ord('q') or key == 27:  # Exit if 'q' or 'Esc' is pressed
                break
        cap.release()  # Release the webcam resource
        cv2.destroyAllWindows()  # Close all OpenCV windows

# Handle invalid choice input
else:
    print("Invalid choice. Please enter 'image' or 'webcam'.")
