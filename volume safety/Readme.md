# Audio Monitoring and WHO Safe Listening Alert System

This program monitors your audio input in real-time and helps you track loud sound levels, notifying you when the audio exceeds certain thresholds. It also ensures that the total listening duration stays within safe limits as per the World Health Organization (WHO) recommendations.

### Features:
- **Real-Time Audio Monitoring:** Captures the audio input from a selected device (e.g., Stereo Mix or loopback device).
- **Volume Level Tracking:** Displays and tracks the current volume in decibels (dB).
- **Loud Sound Alerts:** Sends notifications when the audio level exceeds a threshold (default: -35 dB).
- **Volume Reduction:** Automatically reduces the system volume to 50% if loud audio persists for more than 2 minutes.
- **WHO Safe Listening Timer:** Tracks total listening duration at loud volumes and alerts the user if the total exceeds the WHO safe listening limit (8 hours).
- **Histogram Visualization:** Periodically plots a histogram to show the distribution of the volume levels.

---

### Requirements:
- Python 3.x
- Libraries: 
  - `sounddevice` for audio input
  - `numpy` for numerical calculations
  - `time` for time-related operations
  - `keyboard` for keyboard input detection
  - `plyer` for desktop notifications
  - `matplotlib` for visualizing volume levels
  - `pycaw` for controlling system audio on Windows

You can install the required libraries using `pip`:

```bash
pip install sounddevice numpy time keyboard plyer matplotlib pycaw
```

---

### Usage:
1. **Run the program:** Execute the Python script in your terminal or command prompt.
   
2. **Select Audio Device:** The program will display available audio devices. Choose the appropriate device for monitoring (usually Stereo Mix or a loopback device).
   
3. **Monitor Audio:** The program will start monitoring the audio input in real-time. The volume levels will be displayed on the console, and the program will generate notifications if the audio exceeds certain thresholds.
   
4. **Notifications:**
   - **High Sound Alert:** When the audio level exceeds the defined threshold, you will receive a notification reminding you to lower the volume.
   - **Volume Reduction:** If the loud audio persists for more than 2 minutes, the system volume will be reduced to 50%, and you will be notified.
   - **WHO Safe Listening Alert:** If the total listening time exceeds 8 hours, you will receive a notification warning about unsafe listening duration.

5. **Exit the Program:** Press the `q` key to stop the program at any time.

---

### Customization:
- **Loudness Threshold:** The default loudness threshold is -35 dB. You can change the `DEFAULT_LOUD_DB_LEVEL` constant in the code to set a different threshold.
- **Safe Listening Duration:** The WHO safe listening limit is set to 8 hours. You can adjust this in the `WHO_MAX_LISTENING_DURATION` constant.
- **Volume Reduction Time:** The program reduces the volume if the loud audio lasts for more than 2 minutes. You can adjust this by changing the `REDUCE_VOLUME_THRESHOLD`.

---

### Troubleshooting:
- **No Sound Input Devices Detected:** Ensure your audio devices are correctly set up and the input device (Stereo Mix or loopback) is available.
- **No Notifications:** Check if the `plyer` library is properly installed and that desktop notifications are allowed on your system.

---
