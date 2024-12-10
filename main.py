import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
import subprocess
from datetime import datetime
import random
import musicLibrary

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = "226814c0de644399b97d73b6e9e3db39"
api_key = "17c8620a09e80a6c43adeacbabaae832"

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Searching Google for {query}.")

def tell_random_fact():
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        r.raise_for_status()
        fact = r.json().get('text', '')
        speak(f"Here's a random fact: {fact}")
    except requests.RequestException:
        speak("Sorry, I couldn't fetch a random fact right now.")
        
def get_motivational_quote():
    try:
        r = requests.get("https://type.fit/api/quotes")
        r.raise_for_status()
        quotes = r.json()
        random_quote = random.choice(quotes)
        speak(f"Here's a motivational quote: {random_quote['text']} by {random_quote.get('author', 'Unknown')}")
    except requests.RequestException:
        speak("Sorry, I couldn't fetch a motivational quote right now.")         

def authenticate_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say your name.")
        audio = recognizer.listen(source)
        try:
            user_name = recognizer.recognize_google(audio)
            if user_name.lower() in ["harsh thakur"]:
                speak("Welcome back, Harsh!")
                return True
            else:
                speak("Sorry, I don't recognize your voice.")
                return False
        except sr.UnknownValueError:
            speak("I didn't catch that. Please try again.")
            return False

def specific_information(query):
    try:
        search_url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
        r = requests.get(search_url)
        r.raise_for_status()
        data = r.json()
        
        if data['AbstractText']:
            answer = data['AbstractText']
        elif data['RelatedTopics']:
            answer = data['RelatedTopics'][0]['Text']
        else:
            answer = "I couldn't find a detailed answer to your query."

        speak(answer)
        
    except requests.RequestException:
        speak("Sorry, I couldn't connect to the information service right now.")
    except (KeyError, IndexError):
        speak("Sorry, I couldn't find the information you requested.")

def personalized_greeting():
    hour = datetime.now().hour
    if hour < 12:
        speak("Good morning sir....!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir....!")
    else:
        speak("Good evening sir.......!")

def interactive_feedback():
    speak("Is there anything else you would like to do?")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            response = recognizer.recognize_google(audio).lower()
            if "no" in response or "that's all" in response:
                speak("Alright, I'm here if you need anything!")
            else:
                processCommand(response)
        except sr.UnknownValueError:
            speak("I didn't quite catch that. Let me know if you need anything else.")

def daily_briefing():
    try:
        weather_response = requests.get("http://wttr.in/?format=3")
        weather = weather_response.text.strip()
    except requests.RequestException:
        weather = "Sorry, I couldn't fetch the weather."
    
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    speak(f"Here's your daily briefing: It's {current_time} on {current_date}. {weather}")

# Function to open desktop applications
def open_application(app_name):
    if "notepad" in app_name:
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad.")
    elif "calculator" in app_name:
        subprocess.Popen(["calc.exe"])
        speak("Opening Calculator.")
    elif "paint" in app_name:
        subprocess.Popen(["mspaint.exe"])
        speak("Opening Paint.")
    elif "word" in app_name:
        subprocess.Popen(["start", "winword.exe"], shell=True)
        speak("Opening Microsoft Word.")
    elif "excel" in app_name:
        subprocess.Popen(["start", "excel.exe"], shell=True)
        speak("Opening Microsoft Excel.")
    elif "powerpoint" in app_name:
        subprocess.Popen(["start", "powerpnt.exe"], shell=True)
        speak("Opening Microsoft PowerPoint.")
    elif "camera" in app_name:
        subprocess.Popen(["start", "microsoft.windows.camera:"], shell=True)
        speak("Opening Camera.")
    elif "onenote" in app_name:
        subprocess.Popen(["start", "onenote.exe"], shell=True)
        speak("Opening OneNote.")
    elif "settings" in app_name:
        subprocess.Popen(["start", "ms-settings:"], shell=True)
        speak("Opening Settings.")
    
    else:
        speak(f"Sorry, I can't open {app_name} right now.")

# Function to close desktop applications
def close_application(app_name):
    if "notepad" in app_name:
        os.system("taskkill /f /im notepad.exe")
        speak("Closing Notepad.")
    elif "calculator" in app_name:
        os.system("taskkill /f /im calculator.exe")
        speak("Closing Calculator.")
    elif "paint" in app_name:
        os.system("taskkill /f /im mspaint.exe")
        speak("Closing Paint.")
    elif "word" in app_name:
        os.system("taskkill /f /im winword.exe")
        speak("Closing Microsoft Word.")
    elif "excel" in app_name:
        os.system("taskkill /f /im excel.exe")
        speak("Closing Microsoft Excel.")
    elif "powerpoint" in app_name:
        os.system("taskkill /f /im powerpnt.exe")
        speak("Closing Microsoft PowerPoint.")
    elif "camera" in app_name:
        os.system("taskkill /f /im WindowsCamera.exe")
        speak("Closing Camera.")
    elif "onenote" in app_name:
        os.system("taskkill /f /im onenote.exe")
        speak("Closing OneNote.")
    elif "settings" in app_name:
        os.system("taskkill /f /im SystemSettings.exe")
        speak("Closing Settings.")   
    
    else:
        speak(f"Sorry, I can't close {app_name} right now.")
        
def close_browser_tabs():
    speak("Closing browser tabs...")
    if os.name == "nt":  # For Windows
         os.system("taskkill /F /IM chrome.exe")
         os.system("taskkill /F /IM msedge.exe")
         os.system("taskkill /F /IM firefox.exe")
         os.system("taskkill /F /IM opera.exe")
    else:
         os.system("pkill chrome")
         os.system("pkill firefox")
         os.system("pkill safari")
    speak("All browser tabs have been closed.")


def processCommand(c):
    c = c.lower()
    
    if "search for" in c or "what is" in c or "who is" in c:
        if "search for" in c:
            query = c.split("search for", 1)[1].strip()
        elif "what is" in c:
            query = c.split("what is", 1)[1].strip()
        elif "who is" in c:
            query = c.split("who is", 1)[1].strip()
        specific_information(query)
        
    elif "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook.")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn.")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
        speak("Opening Instagram.")
    elif "open netflix" in c:
        webbrowser.open("https://netflix.com")
        speak("Opening Netflix.")
    elif "open whatsapp" in c:
        webbrowser.open("https://whatsapp.com")
        speak("Opening WhatsApp.")
    elif "open notepad" in c or "open calculator" in c or "open paint" in c or "open word" in c or "open excel" in c or "open powerpoint" in c  or "open camera" in c or "open onenote" in c or "open settings" in c:
        open_application(c)
    elif "close notepad" in c or "close calculator" in c or "close paint" in c or "close word" in c or "close excel" in c or "close powerpoint" in c or "close camera" in c or "close onenote" in c or "close settings"in c:
        close_application(c)
        
    elif "close tabs" in c or "close browser" in c:
        close_browser_tabs()
    elif c.startswith("play"):
        song = c.split(" ")[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}.")
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            r.raise_for_status()
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles[:10]:
                    speak(article['title'])
            else:
                speak("No news articles found.")
        except requests.RequestException:
            speak("Sorry, I couldn't fetch the news right now.")
    elif "joke" in c:
        try:
            r = requests.get("https://official-joke-api.appspot.com/random_joke")
            r.raise_for_status()
            joke = r.json()
            speak(f"Here's a joke: {joke['setup']} {joke['punchline']}")
        except requests.RequestException:
            speak("Sorry, I couldn't fetch a joke right now.")
            
    elif "define" in c:
        try:
            word = c.split("define", 1)[1].strip()
            r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            r.raise_for_status()
            data = r.json()
            meaning = data[0]['meanings'][0]['definitions'][0]['definition']
            speak(f"The definition of {word} is: {meaning}")
        except requests.RequestException:
            speak("Sorry, I couldn't fetch the definition right now.")
        except (IndexError, KeyError):
            speak("Sorry, I couldn't find the definition.")
            
    elif "authenticate" in c:
        if authenticate_user():
            speak("You are authenticated!")
        else:
            speak("Authentication failed.")
            
    elif "time" in c:
        current_time = datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "date" in c:
        current_date = datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}.")
        
    elif "random fact" in c:
        tell_random_fact()
         
    elif "motivate me" in c or "motivation" in c:
        get_motivational_quote()
    
    elif "brief me" in c:
        daily_briefing()

    else:
        search_google(c)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    personalized_greeting()
    daily_briefing()

    while True:
        r = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Listening ...")
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
            wake_word = r.recognize_google(audio)
            
            if "jarvis" in wake_word.lower():
                speak("Hey, Jarvis here...")
                
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio).lower()
                    
                    speak(f"You said: {command}.")
                    processCommand(command)
                    interactive_feedback()
                    
        except sr.UnknownValueError:
            pass  # Ignore if the speech is not recognized
        except sr.RequestError:
            speak("Sorry, I'm having trouble understanding you.")
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, something went wrong.")
