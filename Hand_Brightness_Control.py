import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
import time

# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Get the current screen brightness
current_brightness = sbc.get_brightness(display=0)
if isinstance(current_brightness, list):  # If brightness is returned as a list, take the first element
    current_brightness = current_brightness[0]
smoothing_factor = 0.1  # Factor for smooth transition in brightness change
brightness_range = (10, 100)  # Minimum and maximum brightness range
brightness_lock = False  # Variable to track if brightness is locked
last_hand_detection_time = time.time()  # To track last time a hand was detected for idle detection
idle_lock_timeout = 5  # Timeout for auto-lock in seconds if no hand is detected

# Function to calculate the Euclidean distance between two points
def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Function to check if a finger is extended based on its y-coordinate
def is_finger_extended(finger_tip, wrist):
    return finger_tip.y < wrist.y

# Function to calculate the brightness of the frame based on pixel intensity
def calculate_frame_brightness(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
    avg_brightness = np.mean(gray_frame)  # Calculate the average pixel intensity
    normalized_brightness = np.interp(avg_brightness, [0, 255], brightness_range)  # Normalize to the brightness range
    return normalized_brightness

# Main function to control the screen brightness based on hand gestures
def control_brightness():
    global current_brightness, brightness_lock, last_hand_detection_time
    
    # Open the webcam
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB for processing with MediaPipe
        result = hands.process(rgb_frame)  # Process the frame for hand landmarks
        
        if result.multi_hand_landmarks:  # If hands are detected
            last_hand_detection_time = time.time()  # Reset idle timer
            for hand_landmarks in result.multi_hand_landmarks:
                # Get the thumb and pinky tips
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                
                # Calculate the distance between the thumb and pinky tips
                thumb_to_pinky_dist = calculate_distance(
                    (thumb_tip.x, thumb_tip.y), (pinky_tip.x, pinky_tip.y)
                )
                
                # Toggle lock/unlock if hand is closed (fist gesture)
                if thumb_to_pinky_dist < 0.1:
                    brightness_lock = not brightness_lock
                    time.sleep(0.5)  # Prevent rapid toggling of lock
                
                if not brightness_lock:
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]  # Get wrist position
                    extended_fingers = 0  # Initialize counter for extended fingers
                    
                    # Check if fingers are extended (index, middle, ring, pinky)
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP], wrist):
                        extended_fingers += 1
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP], wrist):
                        extended_fingers += 1
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP], wrist):
                        extended_fingers += 1
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP], wrist):
                        extended_fingers += 1

                    # Fine adjust brightness based on distance between thumb and index finger
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    distance = calculate_distance(
                        (thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y)
                    )
                    # Map the distance to brightness range
                    brightness = np.interp(distance, [0.05, 0.3], brightness_range)
                    current_brightness = (1 - smoothing_factor) * current_brightness + smoothing_factor * brightness
                    
                    # Set the screen brightness
                    try:
                        sbc.set_brightness(int(current_brightness), display=0)
                    except Exception as e:
                        print(f"Error setting brightness: {e}")
                    
                    # Display brightness feedback on the screen
                    cv2.putText(frame, f'Brightness: {int(current_brightness)}%', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                # Display lock/unlock status on the screen
                lock_status = "Locked" if brightness_lock else "Unlocked"
                cv2.putText(frame, f'State: {lock_status}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if brightness_lock else (0, 255, 0), 2)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)  # Draw hand landmarks on the frame
        
        else:  # If no hand detected
            if time.time() - last_hand_detection_time > idle_lock_timeout:  # Check if idle timeout has passed
                brightness_lock = True  # Lock brightness if idle
                auto_brightness = calculate_frame_brightness(frame)  # Adjust brightness based on room lighting
                current_brightness = (1 - smoothing_factor) * current_brightness + smoothing_factor * auto_brightness
                try:
                    sbc.set_brightness(int(current_brightness), display=0)
                except Exception as e:
                    print(f"Error setting auto brightness: {e}")
                cv2.putText(frame, f'Auto Brightness: {int(current_brightness)}%', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Display the frame with overlays
        cv2.imshow("Brightness Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
            break
    
    cap.release()  # Release webcam resources
    cv2.destroyAllWindows()  # Close OpenCV windows

control_brightness()  # Run the brightness control function
