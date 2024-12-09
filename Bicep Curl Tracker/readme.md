# **Bicep Curl Tracker**

This project implements a **real-time bicep curl tracker** using Python, OpenCV, and Mediapipe. It captures live video from a webcam, detects body landmarks using Mediapipe's Pose solution, and calculates the angle at the elbow to count repetitions and provide feedback on the exercise form.

---

## **Features**

1. **Real-time Pose Detection**: Utilizes Mediapipe's Pose model to identify key body landmarks.
2. **Angle Calculation**: Computes the angle at the elbow joint using the positions of the shoulder, elbow, and wrist.
3. **Repetition Counting**: Tracks the number of bicep curls completed by analyzing the elbow's angle transitions.
4. **Exercise Form Feedback**:
   - Prompts the user to fully extend their arm during the "down" phase.
   - Acknowledges a complete curl during the "up" phase.
5. **Customizable Parameters**: Modify angle thresholds for counting reps or adjust the feedback messages to suit your needs.

---

## **Prerequisites**

To run this project, ensure the following tools and libraries are installed:

1. **Python 3.7 or later**
2. Libraries:
   - `opencv-python` (for video processing)
   - `mediapipe` (for pose detection)
   - `numpy` (for mathematical operations)

Install the required libraries using:
```bash
pip install opencv-python mediapipe numpy
```

---

## **How It Works**

1. **Video Capture**: The application uses OpenCV to access the webcam and capture video frames in real-time.
2. **Pose Estimation**:
   - Mediapipe's Pose model detects 33 key body landmarks in each frame.
   - Specific landmarks (shoulder, elbow, and wrist) are extracted for angle calculation.
3. **Angle Calculation**:
   - The angle at the elbow is computed using the coordinates of the shoulder, elbow, and wrist.
   - A trigonometric function (`np.arctan2`) determines the angle between the vectors formed by these points.
4. **Repetition Counting**:
   - A repetition starts when the arm fully extends (angle > 160°).
   - It is counted when the arm fully curls (angle < 30°) after being extended.
5. **Feedback**:
   - The application displays the current angle, rep count, and feedback messages directly on the video feed.

---

## **Usage**

1. Clone or download the repository to your local machine:
   ```bash
   git clone https://github.com/your-repo/bicep-curl-tracker.git
   cd bicep-curl-tracker
   ```
2. Run the script:
   ```bash
   python bicep_curl_tracker.py
   ```
3. Follow these steps for proper operation:
   - Ensure your webcam is enabled.
   - Position yourself within the camera's view with your arm visible.
   - Perform bicep curls, and watch the on-screen feedback and rep count.

4. Press **'q'** to exit the application.

---

## **Code Overview**

### 1. **`calculate_angle()`**
Calculates the angle between three points (shoulder, elbow, and wrist):
- Takes the coordinates of these points as input.
- Uses `np.arctan2` to compute the angle in radians, then converts it to degrees.

### 2. **Main Loop**
- Captures each frame from the webcam.
- Processes the frame to extract pose landmarks.
- Tracks the elbow angle and determines the movement stage (`up` or `down`).
- Updates the repetition count and displays the results.

### 3. **Feedback System**
- Provides corrective guidance:
  - Encourages full arm extension during the "down" phase.
  - Compliments completed curls during the "up" phase.

---



## **Known Issues and Limitations**

1. **Camera Angle**: Proper tracking depends on maintaining a clear, front-facing camera angle where the arm is fully visible.
2. **Lighting Conditions**: Poor lighting may affect pose detection accuracy.
3. **Single Arm**: Currently, the script tracks only the left arm. Modify the code to include the right arm if needed.

---




Enjoy tracking your workouts! 💪
