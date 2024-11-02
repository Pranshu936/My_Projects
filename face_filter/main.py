# Importing required libraries
import cv2  # OpenCV library for image and video processing
import mediapipe as mp  # MediaPipe library for facial landmark detection
import numpy as np  # NumPy library for numerical operations
import datetime  # DateTime library for timestamping saved images
import tkinter as tk  # Tkinter library for GUI
from tkinter import filedialog  # For file dialog to select custom filter images
from threading import Thread  # To run video capture in a separate thread

# Setting up MediaPipe FaceMesh and Drawing utilities
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
mp_drawing = mp.solutions.drawing_utils

# Loading overlay images (face filters) from files
overlay_images = [
    cv2.imread(f'd:/python/face_filter/filter_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(2)
]

# Initial filter settings
current_filter = 0  # Start with the first filter
filter_on = True  # Boolean to toggle filter application

# Setting up the GUI window with instructions
root = tk.Tk()
root.title("Face Filter Instructions")  # Window title
root.geometry("400x600")  # Window size

# Instructions for using the face filter application
instructions = """
Real-Time Face Filter Application with Advanced Features
========================================================
Instructions:
1. Press keys 0 and 1 to switch between different filters.
2. Press 's' to save the current modified image with a timestamp.
3. Press 't' to toggle the filter on/off.
4. Press 'a' to add a new custom filter from file.
5. Press 'q' to exit the application.
"""

# Displaying instructions in the GUI window
instruction_label = tk.Label(root, text=instructions, justify="left", anchor="nw", padx=10, pady=10)
instruction_label.pack(fill="both", expand=True)

# Function to overlay transparent images (filters) onto the video feed
def overlay_transparent(background, overlay, x, y, width=None, height=None):
    # Resizing overlay to match specified width and height
    if width and height:
        overlay = cv2.resize(overlay, (width, height))

    h, w, _ = overlay.shape  # Dimensions of the overlay
    # Adjust dimensions if overlay goes out of bounds
    if y + h > background.shape[0] or x + w > background.shape[1]:
        h = min(h, background.shape[0] - y)
        w = min(w, background.shape[1] - x)
        overlay = overlay[:h, :w]

    # Splitting overlay into color and alpha (transparency) channels
    b, g, r, a = cv2.split(overlay)
    overlay_color = cv2.merge((b, g, r))
    mask = cv2.merge((a, a, a))

    # Applying mask to the background and overlay to combine images
    roi = background[y:y+h, x:x+w]
    img1_bg = cv2.bitwise_and(roi, cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(overlay_color, mask)

    background[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)
    return background

# Function to start video capture and apply filters in real-time
def start_video_capture():
    global current_filter, filter_on
    cap = cv2.VideoCapture(0)  # Start capturing video from the webcam

    while cap.isOpened():
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
        results = face_mesh.process(rgb_frame)  # Process frame to detect face landmarks

        # If face landmarks are detected, proceed with applying filter
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get the coordinates of left and right eyes from landmarks
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]

                h, w, _ = frame.shape  # Get frame dimensions
                left_eye = (int(left_eye.x * w), int(left_eye.y * h))
                right_eye = (int(right_eye.x * w), int(right_eye.y * h))

                # Calculate filter dimensions and position based on eye distance
                width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * 2)
                height = int(width * overlay_images[current_filter].shape[0] / overlay_images[current_filter].shape[1])
                x = left_eye[0] - width // 4
                y = left_eye[1] - height // 2

                # Overlay the selected filter on the frame if filter_on is True
                if filter_on:
                    frame = overlay_transparent(frame, overlay_images[current_filter], x, y, width, height)

        cv2.imshow('Real-Time Face Filter', frame)  # Display the frame with filter

        key = cv2.waitKey(1) & 0xFF  # Wait for key input

        # Key bindings for user actions
        if key in range(ord('0'), ord('1') + 1):  # Switch filters
            current_filter = key - ord('0')
        elif key == ord('s'):  # Save image with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f'captured_image_{timestamp}.png', frame)
            print(f"Image saved as captured_image_{timestamp}.png")

        elif key == ord('t'):  # Toggle filter on/off
            filter_on = not filter_on
        elif key == ord('a'):  # Add a new custom filter from file
            file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                new_filter = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
                if new_filter is not None:
                    overlay_images.append(new_filter)
                    print("Custom filter added!")
        elif key == ord('q'):  # Exit application
            break

    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close OpenCV windows

# Start the video capture in a separate thread to keep GUI responsive
video_thread = Thread(target=start_video_capture)
video_thread.start()

# Start the Tkinter main loop to display the GUI window
root.mainloop()
