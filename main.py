import speech_recognition as sr

recognizer = sr.Recognizer()


commands = {
    "hello": "Hi there! How can I assist you?",
    "goodbye": "Goodbye! Have a great day!",
    "what's your name": "I am your voice assistant.",
    "how are you": "I'm just a bunch of code, but I'm here to help!"
}



def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, the speech service is unavailable.")
            return ""
        




def respond_to_command(command):
    for key in commands:
        if key in command:
            print(commands[key])
            return
    print("Sorry, I don't recognize that command.")

if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if "exit" in command:
            print("Exiting...")
            break
        respond_to_command(command)