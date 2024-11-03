import cv2
import mediapipe as mp
import numpy as np
import datetime
import tkinter as tk
from tkinter import filedialog
from threading import Thread

# Initialize MediaPipe's face mesh for facial landmark detection
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=5, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Load filter images (overlays) from files and store them in a list
overlay_images = [
    cv2.imread(f'd:/python/face_filter/filter_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(3)
]

# Initialize filter settings
current_filter = 0  # Index of the currently selected filter
filter_on = True  # Boolean to toggle filter on/off

# Set up the Tkinter window for displaying instructions
root = tk.Tk()
root.title("Face Filter Instructions")
root.geometry("400x600")

# Define the instructions text for the Tkinter window
instructions = """
Real-Time Face Filter Application with Advanced Features
========================================================
Instructions:
1. Press keys 0 to 2 to switch between different filters.
2. Press 's' to save the current modified image with a timestamp.
3. Press 't' to toggle the filter on/off.
4. Press 'a' to add a new custom filter from file.
5. Press 'q' to exit the application.
"""

# Add the instructions as a label in the Tkinter window
instruction_label = tk.Label(root, text=instructions, justify="left", anchor="nw", padx=10, pady=10)
instruction_label.pack(fill="both", expand=True)

# Function to overlay transparent images on the video frame
def overlay_transparent(background, overlay, x, y, width=None, height=None):
    # Resize the overlay if width and height are provided
    if width and height:
        overlay = cv2.resize(overlay, (width, height))

    # Ensure overlay has an alpha channel; convert if it doesn't
    if overlay.shape[2] == 3:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)

    # Get the dimensions of the overlay image
    h, w, _ = overlay.shape

    # Check if overlay fits within the background; adjust size if necessary
    if y + h > background.shape[0] or x + w > background.shape[1]:
        h = min(h, background.shape[0] - y)
        w = min(w, background.shape[1] - x)
        overlay = overlay[:h, :w]

    # Separate channels and create a mask using the alpha channel
    b, g, r, a = cv2.split(overlay)
    overlay_color = cv2.merge((b, g, r))
    mask = cv2.merge((a, a, a))

    # Define the region of interest (ROI) on the background
    roi = background[y:y+h, x:x+w]

    # Resize mask and overlay if ROI dimensions do not match
    if roi.shape[:2] != mask.shape[:2]:
        mask = cv2.resize(mask, (roi.shape[1], roi.shape[0]))
        overlay_color = cv2.resize(overlay_color, (roi.shape[1], roi.shape[0]))
        
    # Create background and overlay components for blending
    img1_bg = cv2.bitwise_and(roi, cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(overlay_color, mask)

    # Combine the two images and place the result back in the background
    background[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)
    return background

# Function to start capturing video and applying filters
def start_video_capture():
    global current_filter, filter_on

    # Start capturing video from the default camera
    cap = cv2.VideoCapture(0)

    # Main loop for video capture
    while cap.isOpened():
        ret, frame = cap.read()  # Capture a frame
        if not ret:  # Exit if no frame is captured
            break

        # Convert the frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)  # Process the frame to get face landmarks

        # Check if any faces were detected
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract positions for left and right eyes for filter placement
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]

                # Calculate eye coordinates in pixels
                h, w, _ = frame.shape
                left_eye = (int(left_eye.x * w), int(left_eye.y * h))
                right_eye = (int(right_eye.x * w), int(right_eye.y * h))

                # Determine overlay width and height based on eye distance
                width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * 2)
                height = int(width * overlay_images[current_filter].shape[0] / overlay_images[current_filter].shape[1])
                x = left_eye[0] - width // 4
                y = left_eye[1] - height // 2

                # Apply the overlay if the filter is on
                if filter_on and current_filter < len(overlay_images):
                    frame = overlay_transparent(frame, overlay_images[current_filter], x, y, width, height)

        # Display the frame with any overlays applied
        cv2.imshow('Real-Time Face Filter', frame)

        # Handle keypress events for filter operations
        key = cv2.waitKey(1) & 0xFF

        # Switch filters with keys 0 to 2
        if key in (ord('0'), ord('1'), ord('2')):
            current_filter = key - ord('0')
        elif key == ord('s'):
            # Save the current frame with a timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f'captured_image_{timestamp}.png', frame)
            print(f"Image saved as captured_image_{timestamp}.png")
        elif key == ord('t'):
            # Toggle filter on/off
            filter_on = not filter_on
        elif key == ord('a'):
            # Allow user to add a custom filter via file dialog
            file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                new_filter = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
                if new_filter is not None:
                    overlay_images.append(new_filter)
                    print("Custom filter added!")
        elif key == ord('q'):
            # Quit the application
            break

    # Release resources and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Start the video capture function in a separate thread
video_thread = Thread(target=start_video_capture)
video_thread.start()

# Run the Tkinter GUI loop to display instructions
root.mainloop()
