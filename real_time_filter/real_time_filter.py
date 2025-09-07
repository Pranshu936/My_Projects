import cv2
import mediapipe as mp
import numpy as np
import time
import math

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

def apply_filter(frame, filter_type):
    """
    Apply different visual effects (filters) to the input frame.
    The filter_type argument decides which effect to use.
    """
    if filter_type == 1:  # Thermal (heatmap style)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.applyColorMap(gray, cv2.COLORMAP_HOT)

    elif filter_type == 2:  # Grayscale + edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        equalized = cv2.equalizeHist(gray)
        combined = cv2.addWeighted(equalized, 0.7, edges, 0.3, 0)
        return cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)

    elif filter_type == 3:  # High contrast black & white
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        return cv2.cvtColor(clahe.apply(gray), cv2.COLOR_GRAY2BGR)

    elif filter_type == 4:  # Particle effect overlay
        particle_frame = frame.copy()
        h, w, _ = particle_frame.shape
        num_particles = 150
        particle_positions = np.random.randint(0, [w, h], size=(num_particles, 2))
        for i, pos in enumerate(particle_positions):
            hue = (i * 10) % 180
            color = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
            size = np.random.randint(1, 4)
            cv2.circle(particle_frame, tuple(pos), size, tuple(map(int, color)), -1)
        return particle_frame

    elif filter_type == 5:  # Sepia tone
        kernel = np.array([[0.272, 0.543, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    elif filter_type == 6:  # Neon glow
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        neon = cv2.applyColorMap(edges, cv2.COLORMAP_PLASMA)
        return cv2.addWeighted(frame, 0.3, neon, 0.7, 0)

    elif filter_type == 7:  # Vintage film look
        noise = np.random.normal(0, 25, frame.shape).astype(np.uint8)
        vintage = cv2.add(frame, noise)
        vintage[:, :, 0] = np.clip(vintage[:, :, 0] * 0.8, 0, 255)
        vintage[:, :, 1] = np.clip(vintage[:, :, 1] * 1.1, 0, 255)
        vintage[:, :, 2] = np.clip(vintage[:, :, 2] * 1.2, 0, 255)
        return vintage.astype(np.uint8)

    elif filter_type == 8:  # Cyberpunk glitch effect
        b, g, r = cv2.split(frame)
        shift = np.random.randint(-5, 6)
        r_shifted = np.roll(r, shift, axis=1)
        b_shifted = np.roll(b, -shift, axis=1)
        cyberpunk = cv2.merge([b_shifted, g, r_shifted])
        gray_cyber = cv2.cvtColor(cyberpunk, cv2.COLOR_BGR2GRAY)
        cyberpunk = cv2.addWeighted(cyberpunk, 0.8,
                                    cv2.applyColorMap(gray_cyber, cv2.COLORMAP_COOL), 0.2, 0)
        return cyberpunk

    return frame


def apply_filter_to_polygon(frame, filter_type, polygon_points):
    """
    Apply a filter only within a user-defined polygon (hand gestures define the region).
    """
    if polygon_points is None or len(polygon_points) < 3:
        return frame
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [np.array(polygon_points, dtype=np.int32)], 255)
    filtered = apply_filter(frame, filter_type)
    result = frame.copy()
    result[mask == 255] = filtered[mask == 255]
    return result


def get_thumb_index_points(hand_landmarks, w, h):
    """
    Get pixel coordinates of thumb tip and index finger tip for one hand.
    """
    thumb_tip = (int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h))
    index_tip = (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h))
    return thumb_tip, index_tip


def get_gesture_type(hand_landmarks):
    """
    Recognize simple gestures (pointing, pinch, peace, open palm, fist).
    """
    landmarks = [[lm.x, lm.y] for lm in hand_landmarks.landmark]
    finger_tips = [4, 8, 12, 16, 20]
    finger_pips = [3, 6, 10, 14, 18]
    fingers_up = []

    # Thumb check (sideways check instead of vertical like other fingers)
    fingers_up.append(1 if landmarks[finger_tips[0]][0] > landmarks[finger_pips[0]][0] else 0)

    # Other fingers check (vertical direction)
    for i in range(1, 5):
        fingers_up.append(1 if landmarks[finger_tips[i]][1] < landmarks[finger_pips[i]][1] else 0)

    if fingers_up == [0, 1, 0, 0, 0]: return "point"
    elif fingers_up == [1, 1, 0, 0, 0]: return "pinch"
    elif fingers_up == [0, 1, 1, 0, 0]: return "peace"
    elif sum(fingers_up) == 5: return "open_palm"
    elif sum(fingers_up) == 0: return "fist"
    else: return "other"


def create_dynamic_quadrilateral(hand1_points, hand2_points):
    """
    Create a quadrilateral region using two hands (thumb & index points from each hand).
    """
    if hand1_points is None or hand2_points is None:
        return None
    hand1_thumb, hand1_index = hand1_points
    hand2_thumb, hand2_index = hand2_points
    return [hand1_thumb, hand1_index, hand2_index, hand2_thumb]


def check_button_hover(finger_pos, button_positions):
    """
    Check if the fingertip is hovering over a filter selection button.
    """
    for i, (bx, by) in enumerate(button_positions):
        if bx - 40 < finger_pos[0] < bx + 40 and by - 25 < finger_pos[1] < by + 25:
            return i + 1
    return None


def draw_enhanced_ui(frame, selected_filter, apply_mode, hands_count, fps, gesture_info):
    """
    Draws top overlay with system info, filter selection buttons, and gesture feedback box.
    """
    h, w, _ = frame.shape

    # Header background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 80), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    # Title and system status
    cv2.putText(frame, "Enhanced Gesture Filters v2.0", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
    status = f"FPS: {fps:.1f} | Hands: {hands_count} | Mode: {'Active' if apply_mode else 'Standby'}"
    cv2.putText(frame, status, (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Filter buttons (bottom row)
    filters = ["Thermal", "Edge+", "B&W", "Particles", "Sepia", "Neon", "Vintage", "Cyber"]
    num_buttons = len(filters)
    button_width, button_spacing = 80, 15
    total_width = num_buttons * button_width + (num_buttons - 1) * button_spacing
    start_x = (w - total_width) // 2
    button_y = h - 50
    button_positions = [(start_x + (button_width // 2) + i * (button_width + button_spacing), button_y)
                        for i in range(num_buttons)]

    for i, (bx, by) in enumerate(button_positions):
        color = (50, 50, 50) if i + 1 != selected_filter else (0, 200, 0)
        border = (100, 100, 100) if i + 1 != selected_filter else (0, 255, 0)
        text_color = (255, 255, 255) if i + 1 != selected_filter else (0, 0, 0)
        cv2.rectangle(frame, (bx - button_width // 2, by - 25),
                      (bx + button_width // 2, by + 25), color, -1)
        cv2.rectangle(frame, (bx - button_width // 2, by - 25),
                      (bx + button_width // 2, by + 25), border, 2)
        cv2.putText(frame, str(i + 1), (bx - 8, by - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        cv2.putText(frame, filters[i], (bx - 35, by + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1)

    # Gesture feedback box
    if gesture_info:
        cv2.rectangle(frame, (w - 250, 100), (w - 10, 200), (0, 0, 0), -1)
        cv2.rectangle(frame, (w - 250, 100), (w - 10, 200), (100, 100, 100), 2)
        cv2.putText(frame, "Gesture Info:", (w - 240, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        y_offset = 145
        for gesture in gesture_info:
            cv2.putText(frame, gesture, (w - 240, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            y_offset += 20

    return button_positions


class VideoRecorder:
    """
    Handles starting, stopping, and writing video recordings with timestamped filenames.
    """
    def __init__(self):
        self.recording = False
        self.writer = None
        self.start_time = None

    def start_recording(self, frame_shape):
        if not self.recording:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"gesture_filter_recording_{timestamp}.avi"
            self.writer = cv2.VideoWriter(filename, fourcc, 20.0,
                                          (frame_shape[1], frame_shape[0]))
            self.recording = True
            self.start_time = time.time()
            print(f"Started recording: {filename}")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.writer:
                self.writer.release()
                self.writer = None
            duration = time.time() - self.start_time
            print(f"Recording stopped. Duration: {duration:.1f}s")

    def write_frame(self, frame):
        if self.recording and self.writer:
            self.writer.write(frame)


def create_controls_panel():
    """
    Create a side window showing usage instructions and hotkeys.
    """
    panel = np.zeros((250, 500, 3), dtype=np.uint8)
    controls = [
        "Controls:",
        "- Use two hands to create filter region",
        "- Point at buttons to select filters",
        "- Press 'r' to start/stop recording",
        "- Press 'ESC' to exit",
        "- Press '1-8' for direct filter selection"
    ]
    cv2.putText(panel, controls[0], (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    y_offset = 80
    for text in controls[1:]:
        cv2.putText(panel, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        y_offset += 30
    return panel


# ------------------- MAIN APPLICATION -------------------
selected_filter = 1
apply_mode = False
polygon_points, hand1_points, hand2_points = None, None, None
recorder = VideoRecorder()
fps_counter, current_fps = 0, 0
fps_start_time = time.time()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

main_window_name = "Enhanced Gesture Filters v2.0"
controls_window_name = "Controls"

controls_panel = create_controls_panel()
cv2.imshow(controls_window_name, controls_panel)
cv2.moveWindow(controls_window_name, 1000, 0)

is_window_positioned = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # FPS calculation
    fps_counter += 1
    if time.time() - fps_start_time > 1:
        current_fps = fps_counter / (time.time() - fps_start_time)
        fps_counter = 0
        fps_start_time = time.time()

    display_frame = frame.copy()
    tracking_area = np.zeros((h, w, 3), dtype=np.uint8)

    # Hand detection
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    hand_positions, index_finger_positions, detected_hands, gesture_info = [], [], [], []
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            gesture = get_gesture_type(hand_landmarks)
            gesture_info.append(f"Hand {i+1}: {gesture}")
            thumb_pos, index_pos = get_thumb_index_points(hand_landmarks, w, h)
            detected_hands.append((thumb_pos, index_pos))
            index_finger_positions.append(index_pos)
            hand_positions.append((thumb_pos, index_pos))

    # Region of interest using two hands
    if len(detected_hands) >= 2:
        hand1_points, hand2_points = detected_hands[0], detected_hands[1]
        polygon_points = create_dynamic_quadrilateral(hand1_points, hand2_points)
        apply_mode = True
    else:
        apply_mode = False
        polygon_points = None

    # Draw UI and get button positions
    button_positions = draw_enhanced_ui(display_frame, selected_filter, apply_mode,
                                        len(detected_hands), current_fps, gesture_info)

    # Finger hover for filter selection
    for finger_pos in index_finger_positions:
        hovered_filter = check_button_hover(finger_pos, button_positions)
        if hovered_filter:
            selected_filter = hovered_filter
            break

    # Apply filter inside polygon if active
    if apply_mode and polygon_points:
        display_frame = apply_filter_to_polygon(display_frame, selected_filter, polygon_points)
        cv2.polylines(display_frame, [np.array(polygon_points, dtype=np.int32)], True, (0, 255, 0), 2)

    # Hand tracking visualization
    for i, hand_pos in enumerate(hand_positions):
        if hand_pos[0] and hand_pos[1]:
            thumb_pos, index_pos = hand_pos
            color = (0, 255, 0) if i == 0 else (255, 0, 255)
            cv2.circle(tracking_area, thumb_pos, 10, color, -1)
            cv2.circle(tracking_area, index_pos, 10, color, -1)
            cv2.line(tracking_area, thumb_pos, index_pos, color, 3)
            cv2.putText(tracking_area, f"Hand {i+1}", (thumb_pos[0] + 15, thumb_pos[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            distance = np.linalg.norm(np.array(thumb_pos) - np.array(index_pos))
            cv2.putText(tracking_area, f"Dist: {int(distance)}px", (thumb_pos[0] + 15, thumb_pos[1] + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # Combine main view and tracking view
    combined_frame = np.vstack([display_frame, tracking_area])

    # Recording overlay
    if recorder.recording:
        final_h, final_w, _ = combined_frame.shape
        cv2.circle(combined_frame, (final_w - 40, 30), 10, (0, 0, 255), -1)
        cv2.putText(combined_frame, "REC", (final_w - 70, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        recorder.write_frame(combined_frame)

    # Resize for display if too large
    max_display_height = 960
    if combined_frame.shape[0] > max_display_height:
        scale_ratio = max_display_height / combined_frame.shape[0]
        new_width = int(combined_frame.shape[1] * scale_ratio)
        display_sized_frame = cv2.resize(combined_frame, (new_width, max_display_height))
    else:
        display_sized_frame = combined_frame

    cv2.imshow(main_window_name, display_sized_frame)

    # Position windows once
    if not is_window_positioned:
        cv2.moveWindow(main_window_name, 0, 0)
        cv2.moveWindow(controls_window_name, display_sized_frame.shape[1] + 10, 0)
        is_window_positioned = True

    # Keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to quit
        break
    elif key == ord('r'):  # Toggle recording
        if recorder.recording:
            recorder.stop_recording()
        else:
            recorder.start_recording(combined_frame.shape)
    elif ord('1') <= key <= ord('8'):  # Direct filter select
        selected_filter = key - ord('0')

recorder.stop_recording()
cap.release()
cv2.destroyAllWindows()
print("Application closed successfully!")
