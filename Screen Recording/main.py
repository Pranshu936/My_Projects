import cv2
import numpy as np
import pyautogui
import time
import signal
import sys

# Define screen size
SCREEN_SIZE = tuple(pyautogui.size())

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
desired_fps = 30  # Typical frame rate for normal speed video
out = cv2.VideoWriter('video.avi', fourcc, desired_fps, SCREEN_SIZE)
if not out.isOpened():
    print("Error: Could not open VideoWriter.")
    sys.exit()

# Initialize webcam
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()

def signal_handler(sig, frame):
    print("Recording Stopped")
    release_resources()
    sys.exit(0)

def release_resources():
    out.release()
    webcam.release()
    cv2.destroyAllWindows()

def capture_screen_and_webcam():
    while True:
        # Capture screenshot
        img = pyautogui.screenshot()
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Capture webcam frame
        ret, frame = webcam.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Get frame dimensions
        fr_height, fr_width, _ = frame.shape

        # Insert webcam frame into screenshot
        img[0:fr_height, 0:fr_width, :] = frame

        # Display the result
        cv2.imshow('Screen Capture with Webcam', img)
        out.write(img)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Recording Stopped")
            break

        # Frame rate control to match desired FPS
        time.sleep(1 / desired_fps)  # Adjust sleep time to control frame rate

    release_resources()

if __name__ == "__main__":
    # Handle graceful exit
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    capture_screen_and_webcam()
