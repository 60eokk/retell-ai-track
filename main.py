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

# State to manage multi-step interactions
interaction_state = {
    "current_step": None,
    "current_task": None
}

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

# Function to handle complex interactions
def handle_complex_interaction(command):
    if interaction_state["current_step"] == "awaiting_task_name":
        interaction_state["current_task"] = command
        interaction_state["current_step"] = None
        return f"Task '{command}' started."

    if "start a new task" in command:
        interaction_state["current_step"] = "awaiting_task_name"
        return "What task would you like to start?"

    if "what's my next task" in command:
        if interaction_state["current_task"]:
            return f"Your next task is '{interaction_state['current_task']}'."
        else:
            return "You don't have any tasks at the moment."

    return "Sorry, I don't recognize that command."

# Function to respond to recognized command
def respond_to_command(command):
    if interaction_state["current_step"]:
        return handle_complex_interaction(command)
    
    # Define simple commands here
    if "hello" in command:
        return "Hi there! How can I assist you?"
    if "goodbye" in command:
        return "Goodbye! Have a great day!"
    if "what's your name" in command:
        return "I am your voice assistant."
    if "how are you" in command:
        return "I'm just a bunch of code, but I'm here to help!"

    # Handle complex interactions
    return handle_complex_interaction(command)

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