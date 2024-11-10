import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

current_brightness = sbc.get_brightness(display=0)
if isinstance(current_brightness, list):
    current_brightness = current_brightness[0]
smoothing_factor = 0.1
brightness_range = (10, 100)
brightness_lock = False
last_hand_detection_time = time.time()
idle_lock_timeout = 5

def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def is_finger_extended(finger_tip, wrist):
    return finger_tip.y < wrist.y

def calculate_frame_brightness(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_frame)
    normalized_brightness = np.interp(avg_brightness, [0, 255], brightness_range)
    return normalized_brightness

def control_brightness():
    global current_brightness, brightness_lock, last_hand_detection_time
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        
        if result.multi_hand_landmarks:
            last_hand_detection_time = time.time()
            for hand_landmarks in result.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                thumb_to_pinky_dist = calculate_distance(
                    (thumb_tip.x, thumb_tip.y), (pinky_tip.x, pinky_tip.y)
                )
                
                if thumb_to_pinky_dist < 0.1:
                    brightness_lock = not brightness_lock
                    time.sleep(0.5)
                
                if not brightness_lock:
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    extended_fingers = 0
                    
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP], wrist):
                        extended_fingers += 1
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP], wrist):
                        extended_fingers += 1
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP], wrist):
                        extended_fingers += 1
                    if is_finger_extended(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP], wrist):
                        extended_fingers += 1

                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    distance = calculate_distance(
                        (thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y)
                    )
                    brightness = np.interp(distance, [0.05, 0.3], brightness_range)
                    current_brightness = (1 - smoothing_factor) * current_brightness + smoothing_factor * brightness
                    
                    try:
                        sbc.set_brightness(int(current_brightness), display=0)
                    except Exception as e:
                        print(f"Error setting brightness: {e}")
                    
                    cv2.putText(frame, f'Brightness: {int(current_brightness)}%', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                lock_status = "Locked" if brightness_lock else "Unlocked"
                cv2.putText(frame, f'State: {lock_status}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if brightness_lock else (0, 255, 0), 2)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        else:
            if time.time() - last_hand_detection_time > idle_lock_timeout:
                brightness_lock = True
                auto_brightness = calculate_frame_brightness(frame)
                current_brightness = (1 - smoothing_factor) * current_brightness + smoothing_factor * auto_brightness
                try:
                    sbc.set_brightness(int(current_brightness), display=0)
                except Exception as e:
                    print(f"Error setting auto brightness: {e}")
                cv2.putText(frame, f'Auto Brightness: {int(current_brightness)}%', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("Brightness Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

control_brightness()
