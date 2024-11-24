# Screen Capture with Webcam Overlay

This Python program records your screen while displaying the webcam feed overlaid on the top-left corner of the screen. It combines the screen capture with the webcam feed and saves the result as a video file. The program captures the screen and webcam frames at a specified frame rate and can be stopped using a keyboard interrupt or by pressing the 'q' key.

### Features:
- **Screen and Webcam Capture:** Capture the screen along with the webcam feed.
- **Video Recording:** Saves the combined video to a file (`video.avi`).
- **Webcam Overlay:** Displays the webcam feed in the top-left corner of the screen.
- **Graceful Exit:** Handles keyboard interrupts and termination signals to release resources properly.

---

### Requirements:
- Python 3.x
- Libraries:
  - `opencv-python`: For video and image processing (capture, display, and save)
  - `pyautogui`: For screen capture
  - `numpy`: For manipulating images and arrays
  - `time`: For controlling the frame rate
  - `signal`: For handling graceful shutdown

You can install the required libraries using `pip`:

```bash
pip install opencv-python pyautogui numpy
```

---

### Usage:

1. **Run the Program:** Execute the Python script in your terminal or command prompt.
   
   The program will:
   - Capture your screen and display it in a window.
   - Overlay the webcam feed on the top-left corner of the screen.
   - Save the combined video as `video.avi` in the same directory.

2. **Stop Recording:** 
   - Press `q` to stop the recording manually.
   - Alternatively, you can use a keyboard interrupt (Ctrl+C) to stop the recording, and the program will clean up resources gracefully.

---

### How It Works:

1. **Screen Capture:** The program uses `pyautogui.screenshot()` to capture the screen as an image and then processes it into an OpenCV format.
   
2. **Webcam Capture:** The program uses OpenCV's `cv2.VideoCapture(0)` to capture frames from the webcam.

3. **Combining Frames:** Each frame from the webcam is overlaid onto the screen capture at the top-left corner.

4. **Video Saving:** The combined frame is written to a video file using OpenCV's `cv2.VideoWriter()`.

5. **Graceful Shutdown:** The program handles keyboard interrupts and termination signals to ensure that resources are released properly and the video is saved without corruption.

---

### Customization:

- **Frame Rate:** You can modify the `desired_fps` variable to control the frame rate of the video. The default is set to 30 frames per second.
  
- **Output Video Settings:** The video output file name and codec are set in the `cv2.VideoWriter()` function. You can change the `fourcc` codec to adjust the video format if necessary.

- **Webcam Overlay Position:** The webcam frame is inserted at the top-left corner of the screen. You can adjust the position by modifying the `img[0:fr_height, 0:fr_width, :] = frame` line.

---

### Troubleshooting:

- **Webcam Not Detected:** If the webcam is not detected or the frame capture fails, ensure that the webcam is properly connected and accessible.
- **Screen Capture Issues:** If the screen capture is not working as expected, ensure that `pyautogui` is correctly capturing your screen, and check that your display drivers are up-to-date.

