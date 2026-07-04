import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import pygame
import pywhatkit
import traceback
import wikipedia

from openai import OpenAI
from gtts import gTTS
from datetime import datetime

recognizer = sr.Recognizer()
newsapi = " "

music = {
    "humsafar" : "https://youtu.be/0NXnRmoILSs?si=H86bZVv_UZiWl-dh" ,
    "i" : "https://youtu.be/Qg9LxRHLbAk?si=KUCbI17Ehb5MYAbo" ,
    "hola" : "https://youtu.be/De9VIp37CjY?si=A-Lm0RfUfEk9PK96" ,
    "love" : "https://youtu.be/AJtDXIazrMo?si=X5w-1XyEaGyRo7pM" ,
    "boom" : "https://youtu.be/cL0KKSPjZf8?si=q5bGLqXtgCLl751R" ,
    "tum" : "https://youtu.be/LpP4rtjACM8?si=SJg-JhKaQ9GxBJt2" ,
    "crafton" : "https://www.youtube.com/live/Ui0ceEGLa0s?si=w8_Z6UUkgK5vskpK"
}

def speak(text):
    print(f"Nova: {text}")
    engine  = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
def speak_new(text):
    tts = gTTS(text)
    tts.save ('temp.mp3')
    
    
    pygame.mixer.init() #Initialize the Pygame mixer
    pygame.mixer.music.load('temp.mp3') #Load the MP3 File

    pygame.mixer.music.play() #Play the MP3 file

    #Keep the program running untill the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# def aiprocess(command):
#     client = OpenAI(
#     api_key=" ",)
#     completion = client.chat.completions.create(model="gpt-3.5-turbo" , messages=[{"role": "system" , "content" : "You are a Virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud"}, {"role": "user" , "content": command}])
#     return completion.choices[0].message

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "", 1).strip()
        link = music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"I couldn't find {song} in the music library.")
    elif "news" in c.lower():
        try:
            r = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={"country": "us", "apiKey": newsapi},
            timeout=5
        )
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                if not articles:
                    speak("No news found right now.")
                for article in articles[:5]:
                    title = article.get("title")
                    if title:
                        speak(title)
            else:
                speak("Sorry, I couldn't fetch the news.")
        except requests.exceptions.RequestException:
            speak("I'm having trouble connecting to the news service.")
    elif "time" in c.lower():
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in c.lower():
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}")
    elif "day" in c.lower():
        current_day = datetime.now().strftime("%A")
        speak(f"Today is {current_day}")
    elif "send whatsapp message" in c.lower():
        try:
            speak("Whom should I send message to? ")
            with sr.Microphone() as source :
                recognizer.adjust_for_ambient_noise(source,duration=1)
                audio = recognizer.listen(source)
            name = recognizer.recognize_google(audio).lower()
            print("Recognized name:", name)
            contacts = {"mom" : "+91XXXXXXXXXX" ,
                         "dad" : "+91XXXXXXXXXX" , 
                          "adi" : "+91XXXXXXXXXX" ,
                          "brother" : "+91XXXXXXXXXX" }
            if name not in contacts:
                speak("Sorry, Contact not found")
                return
            speak("What is the message")
            with sr.Microphone() as source :
                recognizer.adjust_for_ambient_noise(source,duration=1)
                audio = recognizer.listen(source)
            message = recognizer.recognize_google(audio)
            pywhatkit.sendwhatmsg_instantly(
                contacts[name] ,
                message ,
                wait_time=15 ,
                tab_close=True ,
                close_time= 3
            )
            speak("Your Whatsapp message has been sent successfully.")
        except Exception as e:
            traceback.print_exc()
            speak("Sorry! I couldn't send the message.")
    elif "open wikipedia" in c.lower():
        try:
            speak("What do you want to search on Wikipedia?")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source,duration=1)
                print("Listening...")
                audio = recognizer.listen(source,timeout=5,phrase_time_limit=6)
            query = recognizer.recognize_google(audio)
            query = query.lower()
            query = query.replace("who is" , "")
            query = query.replace("what is" , "")
            query = query.replace("tell me about" , "")
            query = query.strip()
            print("Searching for:" , query)
            speak(f"Searching Wikipedia for {query}")
            result = wikipedia.summary(query,sentences=2)
            speak(result)
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results . Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia.")
        except Exception as e:
            print(e)
            speak("An error occurred while searching Wikipedia")
    # else:
    #     output= aiprocess(c)
    #     speak(output)
if __name__ == "__main__":
    speak("Initializing Nova...")
    #Listen for the wake Word "Jarvis"
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source,duration=1)
                print("Listening...")
                audio = r.listen(source,timeout=5,phrase_time_limit=5)
            word =r.recognize_google(audio)
            if (word.lower()=="nova"):
                speak("Ya")
                with sr.Microphone() as source:
                    print("Nova Active...")
                    audio = r.listen(source)  
                    command =r.recognize_google(audio)
                    processCommand(command)
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except Exception as e:
            print(f"Error: {e}")