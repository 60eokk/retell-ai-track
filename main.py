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

# Define commands and responses
commands = {
    "hello": "Hi there! How can I assist you?",
    "goodbye": "Goodbye! Have a great day!",
    "what's your name": "I am your voice assistant.",
    "how are you": "I'm just a bunch of code, but I'm here to help!",
    "what's the time": "I'm not connected to a clock right now, but I can assist with other tasks.",
    "set a timer for 10 minutes": "Timer set for 10 minutes.",
    "cancel the timer": "Timer canceled.",
    "what's the weather like": "I can't check the weather right now, but you might want to bring an umbrella just in case!",
    "play some music": "I can't play music directly, but try asking your favorite music app.",
    "stop the music": "If music were playing, I would stop it for you.",
    "what's the date today": "I'm not connected to a calendar, but you can always check on your device.",
    "remind me to call mom": "Reminder set to call mom.",
    "show me my reminders": "You have a reminder to call mom.",
    "delete all reminders": "All reminders deleted.",
    "add eggs to my shopping list": "Eggs added to your shopping list.",
    "what's on my shopping list": "Your shopping list includes eggs.",
    "clear my shopping list": "Your shopping list has been cleared.",
    "start a workout": "Workout session started. Let's get moving!",
    "pause my workout": "Workout paused.",
    "end my workout": "Workout session ended. Great job!",
    "what's the news today": "I can't retrieve news directly, but you can check your favorite news site.",
    "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
    "open the door": "I'm not connected to a smart lock, but that would be cool!",
    "close the door": "If I had control, I'd close the door for you."
}

# Function to respond to recognized command
def respond_to_command(command):
    if interaction_state["current_step"]:
        return handle_complex_interaction(command)
    
    for key in commands:
        if key in command:
            return commands[key]

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