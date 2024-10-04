import speech_recognition as sr
import pyttsx3
import os
import subprocess
import datetime

def speak(text):
    """Function to make the assistant speak."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word():
    """Listen until a specific wake word is detected."""
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for the wake word...")
                audio = recognizer.listen(source)

            # Recognize the command and convert it to lower case
            command = recognizer.recognize_google(audio).lower()
            print(f"Detected: {command}")

            # If "hey jarvis" is detected, trigger the actual command listener
            if "hey jarvis" in command:
                speak("Yes, how can I help?")
                return True
        except sr.UnknownValueError:
            print("Wake word not detected. Waiting for another try...")
        except sr.RequestError as e:
            print(f"Request error from speech recognition service: {e}")
            break

def take_command():
    """Take and process commands after the wake word is detected."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        speak("Sorry, I did not catch that.")
    except sr.RequestError as e:
        print(f"Request error: {e}")
        speak("Sorry, the service is currently unavailable.")
    
    return None

def open_application(app_name):
    """Function to open specific applications based on the command."""
    if "chrome" in app_name:
        speak("Opening Chrome")
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        subprocess.Popen([chrome_path])
    elif "notepad" in app_name:
        speak("Opening Notepad")
        subprocess.Popen('notepad.exe')
    elif "file explorer" in app_name:
        speak("Opening File Explorer")
        os.system("explorer")
    elif "calculator" in app_name:
        speak("Opening Calculator")
        subprocess.Popen('calc.exe')
    else:
        speak("Sorry, I don't know how to open that application.")

def close_application(app_name):
    """Function to close specific applications based on the command."""
    if "chrome" in app_name:
        speak("Closing Chrome")
        os.system("taskkill /im chrome.exe /f")
    elif "notepad" in app_name:
        speak("Closing Notepad")
        os.system("taskkill /im notepad.exe /f")
    else:
        speak("Sorry, I can't close that application.")

def tell_time():
    """Function to tell the current time."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}")

# Listening for the wake word first
if listen_for_wake_word():
    while True:
        command = take_command()
        if command:
            if "open" in command:
                if "chrome" in command or "notepad" in command or "file explorer" in command or "calculator" in command:
                    open_application(command)
                else:
                    speak("Sorry, I can't open that.")
            elif "close" in command:
                if "chrome" in command or "notepad" in command:
                    close_application(command)
                else:
                    speak("Sorry, I can't close that.")
            elif "time" in command or "what time" in command:
                tell_time()
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand that command.")
