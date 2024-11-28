import tkinter as tk
from tkinter import *
import pyttsx3

# Initialize pyttsx3 engine 
engine = pyttsx3.init()

# Retrieve available voices
voices = engine.getProperty('voices')

# Preprocess text for better Hinglish pronunciation
def preprocess_text(text):
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
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

# Function to speak the text
def speaknow():
    text = preprocess_text(textv.get())  # Preprocess Hinglish text
    engine.say(text)
    engine.runAndWait()

# Function to change the voice based on user selection
def change_voice(voice_index):
    engine.setProperty('voice', voices[voice_index].id)

# Function to set voice rate and volume
def adjust_voice_settings():
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 1.0)  # Volume

# Set default voice to Indian English if available
def set_default_voice():
    for index, voice in enumerate(voices):
        if "hindi" in voice.name.lower() or "india" in voice.name.lower():
            engine.setProperty('voice', voices[index].id)
            break
    adjust_voice_settings()

root = Tk()

textv = StringVar()

# Frame for Text-to-Speech application
obj = LabelFrame(root, text="Text to Speech (Hinglish)", font=20, bd=1)
obj.pack(fill="both", expand="yes", padx=10, pady=10)

# Label and Entry for Text input
lb1 = Label(obj, text="Text", font=30)
lb1.pack(side=tk.LEFT, padx=5)

text = Entry(obj, textvariable=textv, font=30, width=25, bd=5)
text.pack(side=tk.LEFT, padx=10)

# Speak button
btn = Button(obj, text="Speak", font=20, bg="green", fg="white", command=speaknow)
btn.pack(side=tk.LEFT, padx=10)

# Dropdown menu for voice selection
voice_var = StringVar()
voice_var.set("Select Voice")

voice_menu = OptionMenu(root, voice_var, *[f"Voice {i+1}: {voice.name}" for i, voice in enumerate(voices)], 
                        command=lambda choice: change_voice(int(choice.split()[1])-1))
voice_menu.pack(pady=10)

# Set default voice
set_default_voice()

# Set window title, size, and prevent resizing
root.title("Text to Speech - Hinglish")
root.geometry("480x200")
root.resizable(False, False)

# Start the Tkinter main loop
root.mainloop()
