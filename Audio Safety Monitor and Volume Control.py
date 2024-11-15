import sounddevice as sd
import numpy as np
import time
import keyboard
from plyer import notification
import matplotlib.pyplot as plt
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialization
SAMPLING_RATE = 44100
CHUNK_SIZE = 1024
DEFAULT_LOUD_DB_LEVEL = -35
SILENCE_DB_LEVEL = -90
LOUD_DB_LEVEL = DEFAULT_LOUD_DB_LEVEL
WARNING_INTERVAL = 5
REDUCE_VOLUME_THRESHOLD = 2 * 60
WHO_MAX_LISTENING_DURATION = 8 * 60 * 60
WHO_WARNING_INTERVAL = 60

# Visualization settings
histogram_bins = 50
volume_data = []

# Timer variables
loud_start_time = None
who_timer_start_time = None
total_who_time = 0
last_high_sound_warning_time = 0
last_reduce_volume_warning_time = 0
last_who_warning_time = 0

# System volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def calculate_db(data):
    rms = np.sqrt(np.mean(data ** 2))
    db = 20 * np.log10(rms + 1e-6)
    return db

def notify_user(title, message):
    print(f"\n⚠️ {message} ⚠️")
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )

def plot_histogram():
    plt.clf()
    plt.hist(volume_data, bins=histogram_bins, color='blue', alpha=0.7)
    plt.title("Volume Level Distribution")
    plt.xlabel("Volume (dB)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.pause(0.01)

def reduce_volume():
    volume.SetMasterVolumeLevelScalar(0.5, None)
    print("\n🔊 System volume reduced to 50%.")

# Main Program
print("Available audio devices:")
print(sd.query_devices())

device_index = int(input("Enter the device index for Stereo Mix (or loopback device): "))

try:
    print("Monitoring system audio in the background. Press 'q' to stop.")
    plt.ion()
    plt.figure(figsize=(8, 5))
    running = True

    with sd.InputStream(device=device_index, samplerate=SAMPLING_RATE, blocksize=CHUNK_SIZE, channels=1) as stream:
        while running:
            data, _ = stream.read(CHUNK_SIZE)
            data = np.float32(data)
            db_level = calculate_db(data)

            if db_level < SILENCE_DB_LEVEL:
                print(f"Current Volume: Silence (< {SILENCE_DB_LEVEL:.2f} dB)", end="\r")
                loud_start_time = None
                continue

            print(f"Current Volume: {db_level:.2f} dB", end="\r")
            volume_data.append(db_level)

            if len(volume_data) > 1000:
                volume_data.pop(0)

            current_time = time.time()

            # High sound notifications
            if db_level > LOUD_DB_LEVEL:
                if current_time - last_high_sound_warning_time > WARNING_INTERVAL:
                    notify_user("🔊 High Sound Alert 🔊", f"You are listening at {db_level:.2f} dB. Please lower the volume.")
                    last_high_sound_warning_time = current_time

                if not loud_start_time:
                    loud_start_time = current_time
                elif current_time - loud_start_time > REDUCE_VOLUME_THRESHOLD:
                    if current_time - last_reduce_volume_warning_time > WARNING_INTERVAL:
                        notify_user("🔊 Volume Reduced 🔊", f"Loud sound persisted for over 2 minutes! Volume reduced.")
                        reduce_volume()
                        last_reduce_volume_warning_time = current_time
            else:
                loud_start_time = None

            # WHO timer logic
            if db_level > LOUD_DB_LEVEL:
                if not who_timer_start_time:
                    who_timer_start_time = current_time
                else:
                    total_who_time += current_time - who_timer_start_time
                    who_timer_start_time = current_time
            else:
                who_timer_start_time = None

            if total_who_time > WHO_MAX_LISTENING_DURATION:
                if current_time - last_who_warning_time > WHO_WARNING_INTERVAL:
                    notify_user("⚠️ WHO Safe Listening Alert ⚠️", "You've exceeded the safe listening limit!")
                    last_who_warning_time = current_time

            if len(volume_data) % 50 == 0:
                plot_histogram()

            # Check for 'q' press to exit
            if keyboard.is_pressed('q'):
                print("\nExiting program.")
                running = False

    # Calculate and report total loud sound listening time
    if who_timer_start_time:
        total_who_time += current_time - who_timer_start_time
    total_who_time_hours = total_who_time / 3600
    print(f"\nTotal time listening to loud sound: {total_who_time_hours:.2f} hours")

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
except Exception as e:
    print(f"Error: {e}")
finally:
    plt.ioff()
    plt.close()
    print("Program exited successfully.")
