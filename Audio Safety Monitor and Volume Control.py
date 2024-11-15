# Import necessary libraries
import sounddevice as sd  # For capturing audio input
import numpy as np  # For numerical calculations
import time  # For managing time-related operations
import keyboard  # For detecting keyboard inputs
from plyer import notification  # For desktop notifications
import matplotlib.pyplot as plt  # For plotting histograms
from ctypes import cast, POINTER  # For handling Windows COM objects
from comtypes import CLSCTX_ALL  # Context for Windows COM operations
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # For controlling system audio on Windows

# Constants for audio processing
SAMPLING_RATE = 44100  # Standard audio sampling rate
CHUNK_SIZE = 1024  # Number of audio frames per chunk
DEFAULT_LOUD_DB_LEVEL = -35  # Threshold for loud audio in decibels
SILENCE_DB_LEVEL = -90  # Threshold for silence in decibels
LOUD_DB_LEVEL = DEFAULT_LOUD_DB_LEVEL  # Initial loudness threshold
WARNING_INTERVAL = 5  # Interval (seconds) between consecutive warnings
REDUCE_VOLUME_THRESHOLD = 2 * 60  # Time (seconds) before volume is reduced
WHO_MAX_LISTENING_DURATION = 8 * 60 * 60  # WHO safe listening duration in seconds
WHO_WARNING_INTERVAL = 60  # Interval (seconds) between WHO warnings

# Settings for histogram visualization
histogram_bins = 50  # Number of bins for the histogram
volume_data = []  # List to store decibel levels for plotting

# Timer variables
loud_start_time = None  # Start time for loud audio
who_timer_start_time = None  # Start time for WHO monitoring
total_who_time = 0  # Total time of exposure to loud audio
last_high_sound_warning_time = 0  # Time of the last high-sound warning
last_reduce_volume_warning_time = 0  # Time of the last volume reduction warning
last_who_warning_time = 0  # Time of the last WHO warning

# System volume control initialization (Windows-specific)
# Retrieve the default audio playback device
devices = AudioUtilities.GetSpeakers()
# Activate the interface for audio endpoint volume control
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Function to calculate decibel (dB) levels from audio data
def calculate_db(data):
    # Calculate root mean square (RMS) of the audio data
    rms = np.sqrt(np.mean(data ** 2) + 1e-10)  # Adding small value to avoid division by zero
    # Convert RMS to decibels
    db = 20 * np.log10(rms)
    return db

# Function to display notifications to the user
def notify_user(title, message):
    print(f"\n⚠️ {message} ⚠️")  # Print the message on the console
    notification.notify(
        title=title,  # Title of the notification
        message=message,  # Message body
        timeout=5  # Duration of the notification (seconds)
    )

# Function to plot a histogram of volume data
def plot_histogram():
    plt.clf()  # Clear the current plot
    plt.hist(volume_data, bins=histogram_bins, color='blue', alpha=0.7)  # Plot histogram
    plt.title("Volume Level Distribution")  # Add title
    plt.xlabel("Volume (dB)")  # Label X-axis
    plt.ylabel("Frequency")  # Label Y-axis
    plt.grid(True)  # Add gridlines
    plt.pause(0.01)  # Pause briefly to update the plot

# Function to reduce the system volume to 50%
def reduce_volume():
    volume.SetMasterVolumeLevelScalar(0.5, None)  # Set system volume to 50%
    print("\n🔊 System volume reduced to 50%.")

# Main program execution starts here
print("Available audio devices:")
print(sd.query_devices())  # Display available audio devices

# Prompt user to select a device for monitoring
device_index = int(input("Enter the device index for Stereo Mix (or loopback device): "))

try:
    print("Monitoring system audio in the background. Press 'q' to stop.")  # Instructions
    plt.ion()  # Enable interactive plotting
    plt.figure(figsize=(8, 5))  # Set the size of the histogram figure
    running = True  # Flag to control the monitoring loop

    # Open an audio input stream
    with sd.InputStream(device=device_index, samplerate=SAMPLING_RATE, blocksize=CHUNK_SIZE, channels=1) as stream:
        while running:
            # Read audio data from the stream
            data, _ = stream.read(CHUNK_SIZE)
            data = np.float32(data)  # Convert data to float32 for calculations
            db_level = calculate_db(data)  # Calculate decibel level

            # Check if the audio level is silence
            if db_level < SILENCE_DB_LEVEL:
                print(f"Current Volume: Silence (< {SILENCE_DB_LEVEL:.2f} dB)", end="\r")
                loud_start_time = None  # Reset loud start time
                continue

            # Display the current volume level
            print(f"Current Volume: {db_level:.2f} dB", end="\r")
            volume_data.append(db_level)  # Add the current dB level to the data list

            # Limit the size of the volume data list
            if len(volume_data) > 1000:
                volume_data.pop(0)

            # Get the current time
            current_time = time.time()

            # Check for loud audio and notify the user
            if db_level > LOUD_DB_LEVEL:
                if current_time - last_high_sound_warning_time > WARNING_INTERVAL:
                    notify_user("🔊 High Sound Alert 🔊", f"You are listening at {db_level:.2f} dB. Please lower the volume.")
                    last_high_sound_warning_time = current_time

                # Start tracking loud audio duration
                if not loud_start_time:
                    loud_start_time = current_time
                elif current_time - loud_start_time > REDUCE_VOLUME_THRESHOLD:
                    if current_time - last_reduce_volume_warning_time > WARNING_INTERVAL:
                        notify_user("🔊 Volume Reduced 🔊", f"Loud sound persisted for over 2 minutes! Volume reduced.")
                        reduce_volume()
                        last_reduce_volume_warning_time = current_time
            else:
                loud_start_time = None  # Reset loud start time if audio is no longer loud

            # WHO safe listening timer logic
            if db_level > LOUD_DB_LEVEL:
                if not who_timer_start_time:
                    who_timer_start_time = current_time
                else:
                    total_who_time += current_time - who_timer_start_time
                    who_timer_start_time = current_time
            else:
                who_timer_start_time = None  # Reset WHO timer if audio is no longer loud

            # Notify if WHO safe listening limit is exceeded
            if total_who_time > WHO_MAX_LISTENING_DURATION:
                if current_time - last_who_warning_time > WHO_WARNING_INTERVAL:
                    notify_user("⚠️ WHO Safe Listening Alert ⚠️", "You've exceeded the safe listening limit!")
                    last_who_warning_time = current_time

            # Update the histogram periodically
            if len(volume_data) % 50 == 0:
                plot_histogram()

            # Check for 'q' key press to stop the program
            if keyboard.is_pressed('q'):
                print("\nExiting program.")
                running = False

    # Calculate total time exposed to loud sound
    if who_timer_start_time:
        total_who_time += current_time - who_timer_start_time
    total_who_time_hours = total_who_time / 3600  # Convert seconds to hours
    print(f"\nTotal time listening to loud sound: {total_who_time_hours:.2f} hours")

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")
except Exception as e:
    print(f"Error: {e}")  # Print any unexpected error
finally:
    plt.ioff()  # Turn off interactive plotting
    plt.close()  # Close the plot
    print("Program exited successfully.")  # Program termination message
