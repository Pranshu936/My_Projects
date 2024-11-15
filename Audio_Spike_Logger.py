# Import necessary libraries
import pyaudio  # For capturing audio input
import numpy as np  # For numerical computations
import matplotlib.pyplot as plt  # For live plotting
import datetime  # For timestamping logged events
import sys  # For system-level operations like exiting the script

# Step 1: Initialization
SAMPLING_RATE = 44100  # Audio sampling rate (samples per second)
CHUNK_SIZE = 1024      # Number of audio frames per buffer
THRESHOLD = 0.2        # Threshold for detecting noise spikes (RMS value)

# Initialize PyAudio instance for audio processing
p = pyaudio.PyAudio()

# Open a text file to log detected noise spikes with timestamps
log_file = open("noise_spikes_log.txt", "w")
log_file.write("Timestamp, Noise Level\n")  # Write the header for the log file

# Initialize live plot for real-time noise level visualization
plt.ion()  # Enable interactive mode for live updates
fig, ax = plt.subplots()  # Create a figure and axis for the plot
line, = ax.plot([], [], lw=2)  # Initialize an empty line plot
ax.set_ylim(0, 0.5)  # Set the vertical axis range (adjust for sensitivity)
ax.set_xlim(0, 100)  # Set the horizontal axis range (number of chunks displayed)
ax.set_xlabel("Time (chunks)")  # Label for X-axis
ax.set_ylabel("Noise Level (RMS)")  # Label for Y-axis
plot_data = []  # List to store RMS values for plotting

# Step 2: Setup PyAudio Stream
# Open an audio stream for input
stream = p.open(
    format=pyaudio.paInt16,  # Audio format (16-bit integers)
    channels=1,             # Number of channels (1 for mono audio)
    rate=SAMPLING_RATE,     # Sampling rate in Hz
    input=True,             # Enable input mode
    frames_per_buffer=CHUNK_SIZE  # Number of frames per buffer
)

# Graceful exit handler to close resources and exit the program
def handle_exit():
    stream.stop_stream()  # Stop the audio stream
    stream.close()  # Close the audio stream
    p.terminate()  # Terminate the PyAudio instance
    log_file.close()  # Close the log file
    plt.close()  # Close the plot
    sys.exit(0)  # Exit the program

# Step 3: Noise Measurement Loop
try:
    while True:
        # Read audio data from the stream
        audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)  # Convert buffer to NumPy array
        
        # Calculate RMS (Root Mean Square) for noise level
        # Normalize by dividing by 16384 to increase sensitivity to smaller noise levels
        rms = np.sqrt(np.mean(np.square(audio_data / 16384)))  
        
        # Append the calculated RMS value to the plot data list
        plot_data.append(rms)
        if len(plot_data) > 100:  # Limit the data to the last 100 chunks
            plot_data.pop(0)

        # Step 4: Display Graphically
        # Update the plot with the latest RMS values
        line.set_data(range(len(plot_data)), plot_data)  # Update line data
        ax.set_xlim(0, len(plot_data))  # Adjust X-axis to match data length
        fig.canvas.draw()  # Redraw the canvas
        fig.canvas.flush_events()  # Flush any pending GUI events

        # Step 5: Detect and Log Spikes
        if rms > THRESHOLD:  # Check if the RMS value exceeds the threshold
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp
            log_file.write(f"{timestamp}, {rms}\n")  # Write the spike details to the log file
            log_file.flush()  # Ensure the log is written immediately
            print(f"Spike detected! Timestamp: {timestamp}, Noise Level: {rms}")  # Print spike info to console
except KeyboardInterrupt:
    handle_exit()  # Handle graceful exit when the user interrupts with Ctrl+C
