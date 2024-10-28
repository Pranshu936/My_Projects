import cv2  # Importing the OpenCV library for image processing
import numpy as np  # Importing NumPy for numerical operations
from pyzbar.pyzbar import decode  # Importing the decode function from pyzbar to read barcodes
import os  # Importing the os module for file path operations
import webbrowser  # Importing webbrowser module to open URLs

# Specify the path for the data file
data_file_path = 'myDataFile.text'

# Check if the data file exists; if not, create an empty file
if not os.path.exists(data_file_path):
    with open(data_file_path, 'w') as f:
        f.write('')

# Function to process each frame of the image or video
def process_frame(img):
    # Decode barcodes in the image
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')  # Decode the barcode data
        print("Detected Data:", myData)  # Print the detected data

        # Check if the detected data is a URL
        if myData.startswith(('http://', 'https://')):
            print("Opening URL:", myData)  # Print the URL being opened
            webbrowser.open(myData)  # Open the URL in the web browser
        else:
            print("Storing text data in file.")  # Indicate that text data will be stored
            # Append the decoded text data to the data file
            with open(data_file_path, 'a') as f:
                f.write(myData + '\n')

        # Draw a polygon around the detected barcode in the image
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))  # Reshape the points for drawing
        cv2.polylines(img, [pts], True, (255, 0, 0), 5)  # Draw the polygon

        # Get the rectangle around the barcode to display text
        pts2 = barcode.rect
        # Put the decoded data as text on the image
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return img  # Return the processed image

# Prompt the user to choose between using a static image or webcam
choice = input("Do you want to use a static image or the webcam? Enter 'image' or 'webcam': ").strip().lower()

# If the user chooses 'image'
if choice == 'image':
    image_path = input("Enter the path to the image file: ").strip()  # Get the image file path from the user
    # Check if the provided image path exists
    if os.path.exists(image_path):
        img = cv2.imread(image_path)  # Read the image
        img = process_frame(img)  # Process the image to decode barcodes
        cv2.imshow('Result', img)  # Display the processed image
        cv2.waitKey(0)  # Wait for a key press
        cv2.destroyAllWindows()  # Close the image window
    else:
        print(f"Image file '{image_path}' not found.")  # Notify if the image file doesn't exist
# If the user chooses 'webcam'
elif choice == 'webcam':
    cap = cv2.VideoCapture(0)  # Open the webcam
    cap.set(3, 640)  # Set the width of the video capture
    cap.set(4, 480)  # Set the height of the video capture

    # Loop to continuously capture frames from the webcam
    while True:
        success, img = cap.read()  # Read a frame from the webcam
        if not success:  # Break the loop if the frame is not captured successfully
            break

        img = process_frame(img)  # Process the frame to decode barcodes
        cv2.imshow('Result', img)  # Display the processed frame

        # Exit the loop if the 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

    cap.release()  # Release the webcam resource
    cv2.destroyAllWindows()  # Close all OpenCV windows
else:
    print("Invalid input. Please restart the program and enter 'image' or 'webcam'.")  # Handle invalid input
