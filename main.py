from flask import Flask, render_template, request, jsonify
import sounddevice as sd
import numpy as np
import speech_recognition as sr

app = Flask(__name__)

# Initialize the recognizer
recognizer = sr.Recognizer()

# Sampling rate for recording
samplerate = 16000  # Hertz

# Duration of the recording
duration = 3  # seconds

# Function to capture audio using sounddevice
def record_audio():
    print("Listening...")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    return np.squeeze(recording)

# Function to recognize speech from the recorded audio
def recognize_speech(audio_data):
    try:
        audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Sorry, the speech service is unavailable."

# Define preset commands and their responses
commands = {
    "hello": "Hi there! How can I assist you?",
    "goodbye": "Goodbye! Have a great day!",
    "what's your name": "I am your voice assistant.",
    "how are you": "I'm just a bunch of code, but I'm here to help!"
}

# Function to respond to recognized command
def respond_to_command(command):
    for key in commands:
        if key in command:
            return commands[key]
    return "Sorry, I don't recognize that command."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    audio_data = record_audio()
    command = recognize_speech(audio_data)
    response = respond_to_command(command)
    return jsonify({'command': command, 'response': response})

if __name__ == "__main__":
    app.run(debug=True)