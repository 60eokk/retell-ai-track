import sounddevice as sd
import numpy as np
import speech_recognition as sr

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
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, the speech service is unavailable.")
        return ""

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
            print(commands[key])
            return
    print("Sorry, I don't recognize that command.")

if __name__ == "__main__":
    while True:
        audio_data = record_audio()
        command = recognize_speech(audio_data)
        if "exit" in command:
            print("Exiting...")
            break
        respond_to_command(command)