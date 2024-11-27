# ROI Tracking with MeanShift - Readme

This program allows you to select a region of interest (ROI) in a video feed or file and track it using the **MeanShift algorithm**. The application uses **OpenCV** to capture video, process frames, and perform object tracking.

---

## Features

1. **ROI Selection**: 
   - Manually select an object or area in the video to track by clicking and dragging with the mouse.
   
2. **Object Tracking**:
   - Tracks the selected ROI using the **MeanShift algorithm**, which locates the area with the highest probability of the ROI based on a color histogram.

3. **Real-Time Performance**:
   - Displays the current frame rate (FPS) for tracking performance monitoring.

---

## Requirements

### **Python Version**
- Python 3.x

### **Libraries**
- OpenCV: Install it using:
  ```bash
  pip install opencv-python
  ```

---

## How It Works

1. **Setup**:
   - The program opens the default webcam or a video file. If the camera or file cannot be accessed, the script exits with an error.

2. **ROI Selection**:
   - A mouse callback allows you to click and drag to define the ROI.
   - The ROI is validated for size and non-emptiness before proceeding.

3. **Color Histogram**:
   - The selected ROI is converted to the **HSV color space**.
   - A histogram of the ROI's color is calculated and normalized for backprojection.

4. **Tracking**:
   - The **MeanShift algorithm** iteratively adjusts the position of the ROI in subsequent frames to match the backprojection of the histogram.

5. **Display**:
   - The program displays the tracked ROI as a rectangle on the video feed and overlays the current FPS.

6. **Exit**:
   - Press `q` to exit the program.

---

## How to Run

1. Save the script to a file, e.g., `meanshift_tracking.py`.
2. Run the script:
   ```bash
   python meanshift_tracking.py
   ```
3. The video feed will open in a window titled **"Tracking"**.

4. **Select ROI**:
   - Click and drag with the mouse on the area to track.
   - Release the mouse to finalize the selection.

5. The program will track the selected ROI and display a rectangle around it.

---

## Key Functionality

- **ROI Selection**:
  - The mouse callback `select_roi` captures the coordinates of the ROI.
- **Backprojection**:
  - Converts each frame to HSV and projects the color histogram of the ROI.
- **MeanShift**:
  - Adjusts the ROI's position to match the histogram's highest probability region.

---

## Notes

1. Ensure sufficient lighting and contrast for better tracking performance.
2. The program can be extended to handle occlusion or dynamically adapt the ROI histogram.
3. The program tracks based on color; drastic changes in object appearance can reduce accuracy.

---

Enjoy experimenting with object tracking! 🚀
