from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
from  main import process_cmd

app = Flask(__name__)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Recognize Speech Function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "There was an error connecting to the speech recognition service."

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    user_command = recognize_speech()  # Start listening
    print(f"Recognized Command: {user_command}")

    # Process Command and Get Response
    chatbot_response = process_cmd(user_command)

    # Speak the Response
    speak(chatbot_response)

    # Send Response to Frontend
    return jsonify({"response": chatbot_response})

@app.route('/stop', methods=['POST'])
def stop():
    return jsonify({"response": "Assistant stopped. Goodbye!"})

if __name__ == '__main__':
    app.run(debug=True)
