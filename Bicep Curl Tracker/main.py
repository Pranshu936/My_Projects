import cv2  # OpenCV for video capturing and image processing
import mediapipe as mp  # Mediapipe for pose detection
import numpy as np  # Numpy for mathematical operations

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    """
    Calculate the angle formed by three points.
    :param a: Coordinates of the first point (e.g., shoulder).
    :param b: Coordinates of the second (middle) point (e.g., elbow).
    :param c: Coordinates of the third point (e.g., wrist).
    :return: Angle in degrees between the three points.
    """
    # Convert points to numpy arrays for easy mathematical operations
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # Compute the angle using arctan2 and vector differences
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)  # Convert radians to degrees

    # Ensure angle is always between 0 and 180
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Initialize Mediapipe utilities for pose detection
mp_pose = mp.solutions.pose  # Mediapipe Pose model
mp_drawing = mp.solutions.drawing_utils  # Utility to draw landmarks on the image
pose = mp_pose.Pose()  # Pose object to process pose landmarks

# Initialize variables for tracking exercise
rep_count = 0  # Keeps count of completed bicep curls
stage = None  # Tracks movement stage: "up" or "down"

# Start video capture from the default webcam
cap = cv2.VideoCapture(0)

# Main loop to process video frames
while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:  # Break the loop if the frame cannot be read
        break

    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)

    # Convert the image to RGB format (required by Mediapipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Pose to detect landmarks
    results = pose.process(rgb_frame)

    # Check if any pose landmarks were detected
    if results.pose_landmarks:
        # Extract pose landmarks
        landmarks = results.pose_landmarks.landmark

        # Retrieve coordinates for the left shoulder, elbow, and wrist
        shoulder = [
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
        ]
        elbow = [
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
        ]
        wrist = [
            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
        ]

        # Calculate the angle at the elbow
        angle = calculate_angle(shoulder, elbow, wrist)

        # Display the calculated angle on the video frame
        cv2.putText(
            frame,
            f"Angle: {int(angle)}",  # Convert angle to integer for display
            tuple(np.multiply(elbow, [640, 480]).astype(int)),  # Scale coordinates
            cv2.FONT_HERSHEY_SIMPLEX,  # Font style
            0.6,  # Font size
            (255, 255, 255),  # Font color (white)
            2,  # Thickness
            cv2.LINE_AA,  # Anti-aliased text
        )

        # Bicep curl logic: Count repetitions based on elbow angle
        if angle > 160:  # Arm is fully extended
            stage = "down"  # Set stage to "down"
        if angle < 30 and stage == "down":  # Arm is fully curled after being extended
            stage = "up"  # Set stage to "up"
            rep_count += 1  # Increment the repetition count

        # Display the repetition count on the frame
        cv2.putText(
            frame,
            f"Reps: {rep_count}",  # Display the number of repetitions
            (10, 50),  # Position on the frame
            cv2.FONT_HERSHEY_SIMPLEX,  # Font style
            1.5,  # Font size
            (0, 255, 0),  # Font color (green)
            2,  # Thickness
            cv2.LINE_AA,  # Anti-aliased text
        )

        # Provide feedback on the form during the exercise
        if angle > 160:  # If arm is fully extended
            cv2.putText(
                frame,
                "Good: Extend your arm fully!",  # Feedback message
                (10, 100),  # Position on the frame
                cv2.FONT_HERSHEY_SIMPLEX,  # Font style
                0.8,  # Font size
                (0, 255, 0),  # Font color (green)
                2,  # Thickness
                cv2.LINE_AA,  # Anti-aliased text
            )
        elif angle < 30:  # If arm is fully curled
            cv2.putText(
                frame,
                "Great curl!",  # Feedback message
                (10, 100),  # Position on the frame
                cv2.FONT_HERSHEY_SIMPLEX,  # Font style
                0.8,  # Font size
                (0, 255, 0),  # Font color (green)
                2,  # Thickness
                cv2.LINE_AA,  # Anti-aliased text
            )

    # Draw pose landmarks and connections on the frame
    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display the annotated video frame
    cv2.imshow("Bicep Curl Tracker", frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Release the webcam and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
