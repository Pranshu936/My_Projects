import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pyttsx3
import os

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Retrieve available voices from the pyttsx3 engine
voices = engine.getProperty('voices')

# Function to preprocess Hinglish text for better pronunciation
def preprocess_text(text):
    # Create a dictionary of common Hinglish terms and their phonetic equivalents
    replacements = {
        "namaste": "namastay",
        "bahut": "bahoot",
        "achha": "aacha",
        "hai": "hey",
        "aaj": "aaj",
        "kya": "kyaa",
        "kaise": "kaisay",
        "main": "me",
    }
    # Replace terms in the input text with their phonetic equivalents
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

# Function to speak the input text
def speaknow():
    # Get the input text, preprocess it, and speak it using the pyttsx3 engine
    text = preprocess_text(textv.get())
    engine.say(text)
    engine.runAndWait()

# Function to save the audio of the input text as a .wav file
def save_audio():
    # Get and preprocess the input text
    text = preprocess_text(textv.get())
    # Do nothing if the text is empty or contains only whitespace
    if not text.strip():
        return
    # Open a file dialog to select a location and name for the .wav file
    filepath = filedialog.asksaveasfilename(defaultextension=".wav", 
                                            filetypes=[("WAV files", "*.wav")],
                                            title="Save as")
    # If a file path is selected, save the audio
    if filepath:
        engine.save_to_file(text, filepath)
        engine.runAndWait()

# Function to change the voice based on user selection from the dropdown
def change_voice(voice_index):
    # Set the voice to the selected index
    engine.setProperty('voice', voices[voice_index].id)

# Function to adjust voice speed (rate) and volume
def adjust_voice_settings():
    # Set speech speed to 150 words per minute
    engine.setProperty('rate', 150)
    # Set volume to maximum (1.0)
    engine.setProperty('volume', 1.0)

# Function to set the default voice to an Indian English voice if available
def set_default_voice():
    for index, voice in enumerate(voices):
        # Check if the voice name contains "hindi" or "india"
        if "hindi" in voice.name.lower() or "india" in voice.name.lower():
            # Set the voice to the first matching voice
            engine.setProperty('voice', voices[index].id)
            break
    # Adjust voice settings (speed and volume) after setting the default voice
    adjust_voice_settings()

# Create the main Tkinter window
root = Tk()

# Create a StringVar to hold the input text
textv = StringVar()

# Create a labeled frame for the Text-to-Speech application
obj = LabelFrame(root, text="Text to Speech", font=("Arial", 15), bd=1)
obj.pack(fill="both", expand="yes", padx=10, pady=10)

# Label for the text input field
lb1 = Label(obj, text="Text", font=("Arial", 12))
lb1.pack(side=tk.LEFT, padx=5)

# Entry widget for text input
text = Entry(obj, textvariable=textv, font=("Arial", 12), width=25, bd=5)
text.pack(side=tk.LEFT, padx=10)

# Button to speak the text
btn_speak = Button(obj, text="Speak", font=("Arial", 12), bg="green", fg="white", command=speaknow)
btn_speak.pack(side=tk.LEFT, padx=10)

# Button to save the text-to-speech output as an audio file
btn_save = Button(obj, text="Save", font=("Arial", 12), bg="blue", fg="white", command=save_audio)
btn_save.pack(side=tk.LEFT, padx=10)

# Dropdown menu for selecting a voice
voice_var = StringVar()  # Variable to hold the selected voice
voice_var.set("Select Voice")  # Default text for the dropdown

# Populate the dropdown with available voices
voice_menu = OptionMenu(root, voice_var, *[f"Voice {i+1}: {voice.name}" for i, voice in enumerate(voices)], 
                        command=lambda choice: change_voice(int(choice.split()[1])-1))
voice_menu.pack(pady=10)

# Set the default voice to Indian English if available
set_default_voice()

# Set the window title and size, and prevent resizing
root.title("Text to Speech")
root.geometry("500x250")
root.resizable(False, False)

# Start the Tkinter main loop to display the GUI and handle user interaction
root.mainloop()
