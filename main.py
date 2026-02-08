import speech_recognition as sr
import webbrowser
import subprocess
from gtts import gTTS
import pygame
import os
import time

recognizer = sr.Recognizer()

# ✅ SPEAK FUNCTION (Stable)
def speak(text):
    try:
        print("Jarvis:", text)

        tts = gTTS(text=text, lang='en')
        tts.save("temp.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.2)

        pygame.mixer.music.unload()
        os.remove("temp.mp3")

    except Exception as e:
        print("Speech error:", e)


# ✅ AI FUNCTION (SHORT ANSWERS)
def aiProcess(command):
    try:
        print("Thinking...")

        prompt = f"Answer in one short sentence: {command}"

        result = subprocess.run(
            ["ollama", "run", "phi3", prompt],
            capture_output=True,
            text=True,
            timeout=40
        )

        response = result.stdout.strip()

        # limit length
        response = response[:200]

        if response == "":
            return "I could not understand."

        return response

    except subprocess.TimeoutExpired:
        return "AI is taking too long."

    except Exception as e:
        return "AI error occurred."


# ✅ COMMAND HANDLER
def processCommand(c):

    c = c.lower()

    if "stop" in c or "exit" in c or "bye" in c:
        speak("Goodbye!")
        exit()

    elif "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    else:
        response = aiProcess(c)
        speak(response)


# ✅ MAIN LOOP
if __name__ == "__main__":

    speak("Initializing Jarvis")

    while True:

        try:
            with sr.Microphone() as source:

                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

                word = recognizer.recognize_google(audio)

                if "jarvis" in word.lower():

                    speak("Yes")

                    with sr.Microphone() as source:

                        print("Jarvis Active...")
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)

                        audio = recognizer.listen(
                            source,
                            timeout=8,
                            phrase_time_limit=5
                        )

                        command = recognizer.recognize_google(audio)

                        print("Command:", command)

                        processCommand(command)

        except sr.WaitTimeoutError:
            # prevents spam error
            continue

        except sr.UnknownValueError:
            print("Could not understand audio")

        except Exception as e:
            print("Error:", e)
