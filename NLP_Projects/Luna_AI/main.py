
import random
import webbrowser as wb
import speech_recognition as sr
import pyttsx3
import datetime
import weathers
import gem
import news
import music
import visual_feed

# global variable to track whether assistant should stop 
stop_assistant = False

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Sound producing function
def speak(text):
    engine.setProperty('rate', 200)  # Speed of speech
    tone = engine.getProperty('voices')  # Getting details of current voice
    engine.setProperty('voice', tone[1].id)  # Setting voice (0 for male, 1 for female)
    engine.setProperty('volume', 1)  # Volume should be between 0 and 1
    engine.say(text)
    engine.runAndWait()

def get_dt():
    Now=datetime.datetime.now()

    sdate=Now.strftime("%A, %B %d, %Y")  # Format: Day, Month Date, Year
    stime=Now.strftime("%I:%M %p")  # Format: Hour:Minute AM/PM
    return sdate,stime


def process_cmd(cmd):
    if "open" in cmd.lower():
        site = cmd.lower().split("open ")[1].strip()  #[1]->Selects the second element of the list ["", "instagram"]
        wb.open_new_tab(f"https://www.{site}.com") # because the first element (index 0) is the part before "open ", and the second element (index 1) is the part after "open ".
        speak(f"Opening {site}...")

    elif "play" in cmd.lower():
        if "playlist" in cmd.lower():
            song,link=random.choice(list(music.playlist.items()))
            wb.open_new_tab(link)
            speak(f"playing {song}")

        else:
            Song=cmd.lower().split("play ")[1].strip()
            wb.open(f"https://www.youtube.com/results?search_query={Song}")


    elif "play news" in cmd.lower():
        speak("Fetching the latest news")
        news.get_news(speak)

    elif "date" in cmd.lower():
        sdate, _ =get_dt() #_ this is used to ignore placeholder value
        speak(f"Today's date is {sdate}")

    elif "time" in cmd.lower():
        _, stime = get_dt()
        speak(f"The current time is {stime}")


    elif "weather" in cmd.lower():
        city = cmd.lower().split("weather in ")[1].strip()
    
        weather_info = weathers.get_weather(city)
        speak(weather_info)

    elif "show visual feedback" in cmd.lower():
        data = [1, 2, 3, 4, 5]  # Sample data
        visual_feed.show_visual(data)


    #elif "run vscode" in cmd.lower():
    #   os.startfile(r"C:\Users\himan\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk")

       
    else:
        # Call gimmini for other commands
        output = gem.gimmini(cmd)
        print(output)
        speak(output)




# Main assistant code
if __name__ == '__main__': #to prevent certain code from running when the script is imported as a module. 
    speak("Assistant activated...")

    # Listen only when the word is spoken
    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing...")

        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            word = r.recognize_google(audio)
            print(f"Recognized word: {word}")

            # Luna assistant activation 
            if word.lower() == "luna": # word should be always in small letter
                speak("Hey, tell me")

                # Microphone activation
                with sr.Microphone() as source:
                    print("Listening for commands!")

                    audio = r.listen(source)
                    command = r.recognize_google(audio,language="en-in")
                    speak("ok wait...")
                    process_cmd(command)

            elif word.lower() == "luna stop": 
                speak("Deactivated. Goodbye!")
                break
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {e}")
