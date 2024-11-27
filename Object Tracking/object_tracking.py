import cv2
import numpy as np
import time

# Mouse callback function to select ROI
def select_roi(event, x, y, flags, param):
    global roi_selected, track_window, x_start, y_start, x_end, y_end

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start = x, y
        roi_selected = True

    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        if x_end > x_start and y_end > y_start:
            track_window = (x_start, y_start, x_end - x_start, y_end - y_start)
            roi_selected = False

# Initialize the global variables
roi_selected = False
track_window = (0, 0, 0, 0)
x_start, y_start, x_end, y_end = 0, 0, 0, 0

# Open video capture
cap = cv2.VideoCapture(0)  # Change '0' to 'video.mp4' for video file

# Check if video capture opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a window and bind the mouse callback function
cv2.namedWindow('Tracking')
cv2.setMouseCallback('Tracking', select_roi)

# Initial loop to select the ROI
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # If ROI is being selected, draw rectangle
    if roi_selected:
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)

    cv2.imshow('Tracking', frame)

    # Break loop on 'q' key
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Ensure a valid ROI is selected
if track_window[2] == 0 or track_window[3] == 0:
    print("ROI not selected or invalid, exiting...")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Extract the ROI
x, y, w, h = track_window
roi = frame[y:y+h, x:x+w]

# Check if the ROI is valid (non-empty)
if roi.size == 0:
    print("Error: Selected ROI is empty, exiting...")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Convert the ROI to HSV color space
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Create a histogram and normalize it
roi_hist = cv2.calcHist([hsv_roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Set up the termination criteria for MeanShift
term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

# Frame rate calculation
fps = 0
frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Backproject the histogram onto the frame
    dst = cv2.calcBackProject([hsv_frame], [0, 1], roi_hist, [0, 180, 0, 256], 1)

    # Apply MeanShift to get the new location
    _, track_window = cv2.meanShift(dst, (x, y, w, h), term_criteria)

    # Draw the rectangle around the tracked object
    x, y, w, h = track_window
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Calculate FPS
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()

    # Display FPS
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Tracking', frame)

    # Exit on 'q' key
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release video capture and destroy windows
cap.release()
cv2.destroyAllWindows()
