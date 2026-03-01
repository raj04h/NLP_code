import random
import webbrowser as wb
import speech_recognition as sr
import pyttsx3
import datetime
import weathers
import gem
import news
import music
import pyjokes
import time

# produce speech (engine re-init every call so it never hangs)
def speak(text):
    print(f"Luna says: {text}")  # debug
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume between 0 and 1
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # female
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# to get current date and time
def get_dt():
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")  # Format: Day, Month Date, Year
    time_str = now.strftime("%I:%M %p")       # Format: Hour:Minute AM/PM
    return date_str, time_str

# to process user commands
def process_cmd(cmd):
    response = "I didn't quite get that."  # fallback
    try:
        cmd = cmd.lower()
        if "open" in cmd:
            site = cmd.split("open ")[1].strip()
            wb.open_new_tab(f"https://www.{site}.com")
            response = f"Opening {site}..."

        elif "play" in cmd:
            if "playlist" in cmd:
                song, link = random.choice(list(music.playlist.items()))
                wb.open_new_tab(link)
                response = f"Playing {song}"
            else:
                song = cmd.split("play ")[1].strip()
                wb.open(f"https://www.youtube.com/results?search_query={song}")
                response = f"Playing {song}."

        elif "play news" in cmd:
            response = "Fetching the news."
            news.get_news(speak)

        elif "date" in cmd:
            date_str, _ = get_dt()
            response = f"Today's date is {date_str}"

        elif "time" in cmd:
            _, time_str = get_dt()
            response = f"The current time is {time_str}"

        elif "weather" in cmd:
            city = cmd.split("weather in ")[1].strip()
            weather_info = weathers.get_weather(city)
            response = weather_info

        elif "joke" in cmd:
            response = pyjokes.get_joke()

        elif "write note" in cmd.lower():
            speak("What should I write down?")
            with sr.Microphone() as source:
                note = recognizer.listen(source)
                note_text = recognizer.recognize_google(note)

            with open("notes.txt", "a") as file:
                file.write(f"{datetime.datetime.now()}: {note_text}\n")
            response = "Note saved successfully!"

        else:
            response = gem.gimmini(cmd)

    except Exception as e:
        print(f"Error processing command: {e}")
        response = "Something went wrong while processing your request."

    return response

# to greet based on the time of day
def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 21:
        return "Good evening!"
    else:
        return "Hey!"

# Starting of Assistant
if __name__ == '__main__':
    recognizer = sr.Recognizer() 
    greeting = greet_user()
    speak(f"{greeting} Assistant activated...")

    # Continuous listening for commands
    while True:
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Say something!")
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio).lower()
            print(f"Recognized word: {word}")

            # Luna Word detected
            if word == "Lisa":
                speak("Hey, tell me")
                time.sleep(0.5)  # pause so TTS finishes

                with sr.Microphone() as source:
                    command_audio = recognizer.listen(source, phrase_time_limit=5)

                try:
                    command = recognizer.recognize_google(command_audio)
                    speak("Okay, wait...")
                    response = process_cmd(command)
                    speak(response)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that. Can you repeat?")
                except sr.RequestError:
                    speak("Unable to connect to service.")

            # Luna stop detected
            elif word == "mona stop":
                speak("Deactivated. Goodbye Himanshu!")
                break

        except sr.UnknownValueError:
            speak("Sorry, I didn't hear that clearly.")
        except sr.RequestError:
            speak("Unable to connect to service.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("Something went wrong. Please try again.")
