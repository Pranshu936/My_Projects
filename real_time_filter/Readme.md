
# ✋ Enhanced Gesture Filters v2.0 🎥✨

Bring your webcam to life with **real-time hand gesture–controlled video filters**!  
This project uses **[MediaPipe](https://github.com/google/mediapipe)** and **OpenCV** to let you:

- 🖐️ Control filters with your **hands & gestures**
- 🎨 Apply **8 unique visual effects** (thermal, neon glow, cyberpunk, etc.)
- 🖼️ Select filters by simply pointing at **on-screen buttons**
- 🖼️ Apply filters inside **dynamic polygons** created with two hands
- ⏺️ **Record videos** with filters applied
- 🖥️ Enjoy an **enhanced UI overlay** with FPS counter, gesture feedback, and controls

---

## 🚀 Features

✅ **Gesture Recognition**
- Point, Pinch, Peace ✌️, Open Palm 🖐️, and Fist ✊  
- Automatically detects **1 or 2 hands**  

✅ **Filter Arsenal (1–8)**
1. 🌡️ Thermal  
2. ⚡ Edge+ Grayscale  
3. 🖤 High Contrast B&W  
4. ✨ Particle Overlay  
5. 📼 Sepia Tone  
6. 🌌 Neon Glow  
7. 🎞️ Vintage Film  
8. 🕶️ Cyberpunk Glitch  

✅ **UI Goodies**
- On-screen filter buttons (hover with finger to select)  
- Gesture info box  
- Recording indicator 🔴  

✅ **Recording**
- Press **`r`** to toggle recording  
- Saves `.avi` files with timestamped names  

---



## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/gesture-filters.git
cd gesture-filters

# Install dependencies
pip install opencv-python mediapipe numpy
````

---

## ▶️ Usage

Run the app:

```bash
python gesture_filters.py
```

🎮 **Controls:**

* ✌️ Use **two hands** to create a filter region (dynamic polygon)
* 👉 Point at bottom buttons to switch filters
* 🎥 Press **`r`** → Start/Stop recording
* 🔢 Press **1–8** → Direct filter selection
* ❌ Press **ESC** → Exit

---

## 🖥️ UI Layout

* **Top bar** → FPS, active mode, hand count
* **Bottom row** → Filter buttons
* **Right panel** → Gesture feedback
* **Second view** → Tracking visualization

---

## 📹 Example 




<img width="910" height="827" alt="Screenshot 2025-09-07 001121" src="https://github.com/user-attachments/assets/aa08bc00-3022-43e2-b20e-fc5383edbe35" />


## ⭐ Support

If you like this project:

* Star ⭐ the repo
* Share 📨 with friends
* Contribute 💻 pull requests

Made with ❤️ using **Python, OpenCV, and MediaPipe**

