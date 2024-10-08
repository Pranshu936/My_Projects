import tkinter as tk
from tkinter import *
import pyttsx3

# Initialize pyttsx3 engine (without specifying driverName)
engine = pyttsx3.init()

def speaknow():
    engine.say(textv.get())
    engine.runAndWait()

root = Tk()

textv = StringVar()

# Frame for Text-to-Speech application
obj = LabelFrame(root, text="Text to Speech", font=20, bd=1)
obj.pack(fill="both", expand="yes", padx=10, pady=10)

# Label and Entry for Text input
lb1 = Label(obj, text="Text", font=30)
lb1.pack(side=tk.LEFT, padx=5)

text = Entry(obj, textvariable=textv, font=30, width=25, bd=5)
text.pack(side=tk.LEFT, padx=10)

# Speak button
btn = Button(obj, text="Speak", font=20, bg="green", fg="white", command=speaknow)
btn.pack(side=tk.LEFT, padx=10)

# Set window title, size, and prevent resizing
root.title("Text to Speech")
root.geometry("480x200")
root.resizable(False, False)

# Start the Tkinter main loop
root.mainloop()
