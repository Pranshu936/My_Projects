import cv2
import mediapipe as mp
import numpy as np
import datetime
import tkinter as tk
from tkinter import filedialog
from threading import Thread

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
mp_drawing = mp.solutions.drawing_utils

overlay_images = [
    cv2.imread(f'd:/python/face_filter/filter_{i}.png', cv2.IMREAD_UNCHANGED) for i in range(2)
]

current_filter = 0
filter_on = True

root = tk.Tk()
root.title("Face Filter Instructions")
root.geometry("400x600")

instructions = """
Real-Time Face Filter Application with Advanced Features
========================================================
Instructions:
1. Press keys 0 and 1 to switch between different filters.
2. Press 's' to save the current modified image with a timestamp.
3. Press 't' to toggle the filter on/off.
4. Press 'a' to add a new custom filter from file.
5. Press 'q' to exit the application.
"""

instruction_label = tk.Label(root, text=instructions, justify="left", anchor="nw", padx=10, pady=10)
instruction_label.pack(fill="both", expand=True)

def overlay_transparent(background, overlay, x, y, width=None, height=None):
    if width and height:
        overlay = cv2.resize(overlay, (width, height))

    h, w, _ = overlay.shape
    if y + h > background.shape[0] or x + w > background.shape[1]:
        h = min(h, background.shape[0] - y)
        w = min(w, background.shape[1] - x)
        overlay = overlay[:h, :w]

    b, g, r, a = cv2.split(overlay)
    overlay_color = cv2.merge((b, g, r))
    mask = cv2.merge((a, a, a))

    roi = background[y:y+h, x:x+w]
    img1_bg = cv2.bitwise_and(roi, cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(overlay_color, mask)

    background[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)
    return background

def start_video_capture():
    global current_filter, filter_on
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]

                h, w, _ = frame.shape
                left_eye = (int(left_eye.x * w), int(left_eye.y * h))
                right_eye = (int(right_eye.x * w), int(right_eye.y * h))

                width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * 2)
                height = int(width * overlay_images[current_filter].shape[0] / overlay_images[current_filter].shape[1])
                x = left_eye[0] - width // 4
                y = left_eye[1] - height // 2

                if filter_on:
                    frame = overlay_transparent(frame, overlay_images[current_filter], x, y, width, height)

        cv2.imshow('Real-Time Face Filter', frame)

        key = cv2.waitKey(1) & 0xFF

        if key in range(ord('0'), ord('1') + 1):
            current_filter = key - ord('0')
        elif key == ord('s'):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f'captured_image_{timestamp}.png', frame)
            print(f"Image saved as captured_image_{timestamp}.png")

        elif key == ord('t'):
            filter_on = not filter_on
        elif key == ord('a'):
            file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                new_filter = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
                if new_filter is not None:
                    overlay_images.append(new_filter)
                    print("Custom filter added!")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

video_thread = Thread(target=start_video_capture)
video_thread.start()

root.mainloop()
