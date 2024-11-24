# Hand Gesture Based Screen Brightness Control

This program uses hand gestures to control the screen brightness of your computer. It leverages a webcam for real-time hand tracking and adjusts the brightness based on finger positions and hand gestures. You can lock and unlock the brightness control using a fist gesture, and the brightness can be adjusted by the distance between your thumb and index finger. If no hand is detected for a while, the program will automatically adjust the brightness based on the surrounding lighting.

### Features:
- **Hand Gesture Control:** Control the screen brightness by extending or moving your fingers.
- **Lock/Unlock Brightness:** Use a fist gesture to lock or unlock the brightness adjustments.
- **Automatic Brightness Adjustment:** Adjusts screen brightness based on the ambient lighting if no hand is detected.
- **Smooth Brightness Transition:** Smooth transitions between brightness levels to prevent abrupt changes.
- **Idle Timeout:** Locks the brightness control after a period of no hand detection.

---

### Requirements:
- Python 3.x
- Libraries:
  - `opencv-python`: For real-time video capture and image processing
  - `mediapipe`: For hand tracking and gesture recognition
  - `numpy`: For mathematical calculations (e.g., distance calculation)
  - `screen_brightness_control`: For controlling screen brightness
  - `time`: For tracking the timing of hand gestures and idle states

You can install the required libraries using `pip`:

```bash
pip install opencv-python mediapipe numpy screen-brightness-control
```

---

### Usage:

1. **Run the program:** Execute the Python script in your terminal or command prompt. Ensure your webcam is properly connected.
   
2. **Control Brightness Using Gestures:**
   - **Thumb and Index Finger Distance:** Adjust the brightness by moving your thumb and index finger. The closer they are, the dimmer the screen becomes.
   - **Fist Gesture (Lock/Unlock):** Make a fist to toggle the brightness lock. When locked, the brightness cannot be adjusted by gestures.
   - **Idle Timeout:** If no hand is detected for a few seconds, the brightness control will lock automatically, and the brightness will be adjusted based on ambient lighting.

3. **Display Feedback:** The program will display the current brightness percentage and the lock status (locked/unlocked) on the screen.

4. **Exit the Program:** Press the 'q' key to exit the program at any time.

---

### Customization:

- **Brightness Range:** You can adjust the `brightness_range` variable to set the minimum and maximum screen brightness.
- **Smoothing Factor:** The `smoothing_factor` controls how smooth the transition is when adjusting brightness. You can modify this to make the brightness adjustment more or less responsive.
- **Idle Timeout:** The `idle_lock_timeout` variable sets the time (in seconds) before the brightness is locked due to inactivity.

---

### How It Works:

1. **Hand Detection:** The program uses MediaPipe’s hand tracking model to detect and track hand landmarks in real time.
2. **Brightness Control:** 
   - The program uses the `screen_brightness_control` library to adjust screen brightness.
   - The distance between the thumb and index finger determines the brightness level.
   - If the thumb and pinky distance is small (fist gesture), the brightness lock is toggled.
3. **Automatic Adjustment:** If no hand is detected for a defined period, the program adjusts the brightness based on the average brightness of the captured frame (ambient light).

---

### Troubleshooting:

- **No Hand Detected:** Make sure that your hands are visible in the camera view, and try adjusting the camera angle if needed.
- **Brightness Not Changing:** Ensure that the `screen_brightness_control` library is compatible with your system and screen brightness settings.
- **Performance Issues:** If the frame rate is too low, reduce the resolution or adjust the program’s settings to improve performance.

