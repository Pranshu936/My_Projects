

import openai
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
from gtts import gTTS
import os
from playsound import playsound

# OpenAI API Key - Replace with your own key
openai.api_key = 'Replace with your own key'

# Parameters for recording audio
SAMPLE_RATE = 16000  # Sample rate for sounddevice
DURATION = 8  # Duration in seconds for recording

# Function to record audio using sounddevice
def record_audio():
    print("Recording...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    write("input.wav", SAMPLE_RATE, audio)  # Save as WAV file
    print("Recording finished.")
    return "input.wav"

# Function to recognize speech from the recorded audio
def listen_to_voice():
    recognizer = sr.Recognizer()
    audio_file = record_audio()

    # Load the recorded audio into SpeechRecognition
    with sr.AudioFile(audio_file) as source:
        print("Recognizing...")
        audio_data = recognizer.record(source)
        try:
            question = recognizer.recognize_google(audio_data)
            print(f"You asked: {question}")
            return question
        except sr.UnknownValueError:
            return "Sorry, I didn't get that."

# Function to interact with GPT model to get a response
def get_ai_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can switch to "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        max_tokens=100
    )
    return response.choices[0].message["content"]

# Function to convert text to speech and play it
def speak_response(response_text):
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")

if __name__ == "__main__":
    # Main process
    question = listen_to_voice()
    if question:
        ai_response = get_ai_response(question)
        print(f"AI Response: {ai_response}")
        speak_response(ai_response)
