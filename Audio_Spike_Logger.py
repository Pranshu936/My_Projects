import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys

# Step 1: Initialization
SAMPLING_RATE = 44100  # Sample rate in Hz
CHUNK_SIZE = 1024      # Number of audio frames per buffer
THRESHOLD = 0.2        # Lower threshold for increased sensitivity

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open file to log spikes
log_file = open("noise_spikes_log.txt", "w")
log_file.write("Timestamp, Noise Level\n")

# Initialize live plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 0.5)  # Adjust vertical range for sensitivity
ax.set_xlim(0, 100)
ax.set_xlabel("Time (chunks)")
ax.set_ylabel("Noise Level (RMS)")
plot_data = []

# Step 2: Setup PyAudio Stream
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLING_RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE
)


# Graceful exit handler
def handle_exit():
    stream.stop_stream()
    stream.close()
    p.terminate()
    log_file.close()
    plt.close()
    sys.exit(0)

# Step 3: Noise Measurement Loop
try:
    while True:
        # Read audio data
        audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)
        
        # Calculate RMS with higher sensitivity
        rms = np.sqrt(np.mean(np.square(audio_data / 16384)))  # Normalize to a smaller range for higher sensitivity
        
        # Append to plot data
        plot_data.append(rms)
        if len(plot_data) > 100:
            plot_data.pop(0)

        # Step 4: Display Graphically
        line.set_data(range(len(plot_data)), plot_data)
        ax.set_xlim(0, len(plot_data))
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Step 5: Detect and Log Spikes
        if rms > THRESHOLD:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp}, {rms}\n")
            log_file.flush()
            print(f"Spike detected! Timestamp: {timestamp}, Noise Level: {rms}")
except KeyboardInterrupt:
    handle_exit()
