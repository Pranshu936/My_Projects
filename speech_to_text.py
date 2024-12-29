import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import threading
import os

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Function to process audio and perform speech-to-text and sentiment analysis
def process_audio(audio):
    recognizer = sr.Recognizer()
    try:
        # Convert speech to text using Google's speech recognition API
        transcription = recognizer.recognize_google(audio)
        # Perform sentiment analysis on the transcribed text
        sentiment = sentiment_analyzer.polarity_scores(transcription)
        return transcription, sentiment
    except sr.UnknownValueError:
        # Handle case when speech is unintelligible
        return "Could not understand audio", {}
    except sr.RequestError as e:
        # Handle case when the API request fails
        return f"Request failed: {e}", {}

# Function to start real-time transcription
def start_real_time_transcription():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Function to handle the transcription in a separate thread
    def transcribe():
        with microphone as source:
            # Adjust for background noise
            recognizer.adjust_for_ambient_noise(source)
            messagebox.showinfo("Info", "Start speaking...")
            try:
                # Listen to the audio input from the microphone
                audio = recognizer.listen(source, timeout=10)
                # Process the audio to get transcription and sentiment
                transcription, sentiment = process_audio(audio)
                # Display the results in the text box
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Transcription:\n{transcription}\n\n")
                result_text.insert(tk.END, f"Sentiment Analysis:\n{sentiment}")
                # Enable the save button
                save_button.config(state=tk.NORMAL)
            except Exception as e:
                # Show an error message in case of failure
                messagebox.showerror("Error", f"Failed to process audio: {e}")

    # Run the transcription in a separate thread to keep the GUI responsive
    threading.Thread(target=transcribe).start()

# Function to upload an audio file and perform transcription
def upload_audio_file():
    # Open a file dialog to select an audio file
    file_path = filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*"))
    )
    if not file_path:
        return

    # Ensure the selected file is a WAV file
    if not file_path.lower().endswith(".wav"):
        messagebox.showerror("Error", "Only WAV files are supported.")
        return

    recognizer = sr.Recognizer()
    try:
        # Read the audio file and process it
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            transcription, sentiment = process_audio(audio)
            # Display the results in the text box
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Transcription:\n{transcription}\n\n")
            result_text.insert(tk.END, f"Sentiment Analysis:\n{sentiment}")
            # Enable the save button
            save_button.config(state=tk.NORMAL)
    except Exception as e:
        # Show an error message in case of failure
        messagebox.showerror("Error", f"Failed to process file: {e}")

# Function to save the transcription results to a file
def save_transcription():
    # Get the text content from the results text box
    transcription_data = result_text.get(1.0, tk.END).strip()
    if not transcription_data:
        messagebox.showwarning("Warning", "No transcription available to save.")
        return

    # Open a file dialog to save the results as a text file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Save Transcription"
    )
    if file_path:
        try:
            # Write the transcription data to the selected file
            with open(file_path, "w") as file:
                file.write(transcription_data)
            messagebox.showinfo("Success", f"Transcription saved successfully to {file_path}")
        except Exception as e:
            # Show an error message in case of failure
            messagebox.showerror("Error", f"Failed to save transcription: {e}")

# Tkinter GUI Design
root = tk.Tk()
root.title("Advanced Speech-to-Text Converter")
root.geometry("700x550")
root.configure(bg="white")

# Header section
header_label = tk.Label(
    root, text="Advanced Speech-to-Text Converter", font=("Arial", 20, "bold"), bg="purple", fg="white"
)
header_label.pack(fill=tk.X)

# Real-Time Transcription Section
real_time_frame = tk.Frame(root, bg="white", pady=20)
real_time_frame.pack(fill=tk.X)

real_time_label = tk.Label(real_time_frame, text="Real-Time Transcription", font=("Arial", 14), bg="white")
real_time_label.pack()

real_time_button = tk.Button(
    real_time_frame, text="Start Transcription", font=("Arial", 12), bg="purple", fg="white",
    command=start_real_time_transcription
)
real_time_button.pack(pady=10)

# Divider
divider = tk.Frame(root, height=2, bg="lightgray", relief=tk.SUNKEN)
divider.pack(fill=tk.X, pady=10)

# Upload Audio File Section
upload_frame = tk.Frame(root, bg="white", pady=20)
upload_frame.pack(fill=tk.X)

upload_label = tk.Label(upload_frame, text="Upload Audio File", font=("Arial", 14), bg="white")
upload_label.grid(row=0, column=0, columnspan=3, pady=5)

# Dropdown for selecting language (currently non-functional, placeholder)
language_var = tk.StringVar(value="English (US)")
language_dropdown = ttk.Combobox(
    upload_frame, textvariable=language_var, values=["English (US)", "English (UK)", "Spanish", "French"],
    state="readonly", font=("Arial", 12), width=15
)
language_dropdown.grid(row=1, column=1, padx=10)

upload_button = tk.Button(
    upload_frame, text="Upload and Transcribe", font=("Arial", 12), bg="purple", fg="white",
    command=upload_audio_file
)
upload_button.grid(row=1, column=2, padx=10)

# Divider
divider2 = tk.Frame(root, height=2, bg="lightgray", relief=tk.SUNKEN)
divider2.pack(fill=tk.X, pady=10)

# Results Section
result_label = tk.Label(root, text="Results:", font=("Arial", 14), bg="white")
result_label.pack(pady=5)

result_text = tk.Text(root, height=10, font=("Arial", 12), wrap=tk.WORD)
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Save Button
save_button = tk.Button(
    root, text="Save Transcription", font=("Arial", 12), bg="green", fg="white", command=save_transcription
)
save_button.pack(pady=10)
save_button.config(state=tk.DISABLED)  # Initially disabled

# Run the Tkinter event loop
root.mainloop()
