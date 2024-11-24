import cv2
import numpy as np

config_path = 'd:/python/object_detection/yolov3.cfg'
weights_path = 'd:/python/object_detection/yolov3.weights'
classes_path = 'd:/python/object_detection/yolov3.txt'

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, f"{label}: {confidence:.2f}", (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

with open(classes_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
net = cv2.dnn.readNet(weights_path, config_path)

choice = input("Enter 'image' to use an image file or 'webcam' to use the webcam: ").strip().lower()

def process_frame(frame):
    Height, Width = frame.shape[:2]
    scale = 0.00392
    blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    if len(indices) > 0:
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box
            draw_prediction(frame, class_ids[i], confidences[i], x, y, x + w, y + h)

    return frame

if choice == 'image':
    image_path = input("Enter the path to the image file: ").strip()
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image from {image_path}. Please check the file path.")
    else:
        processed_image = process_frame(image)
        cv2.imshow("Object Detection - Image", processed_image)
        cv2.imwrite("object-detection-output.jpg", processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

elif choice == 'webcam':
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from webcam.")
                break
            processed_frame = process_frame(frame)
            cv2.imshow("Object Detection - Webcam", processed_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
else:
    print("Invalid choice. Please enter 'image' or 'webcam'.")
