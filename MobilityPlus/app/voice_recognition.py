from typing import Any

import pyttsx3
import speech_recognition as sr
from speech_recognition import WaitTimeoutError


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        # speak("Say something:")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=2)  # Listen for up to 2 or 5 seconds
        except WaitTimeoutError:
            print("Timeout. Waiting for input...")
            return None

    try:
        command: list[Any] | tuple[Any, Any] | Any = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()  # Convert the command to lowercase for consistency
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Error with the API request; {e}")
        return None


if __name__ == "__main__":
    while True:
        command = recognize_speech()

        if command:
            # Add your logic to interpret the command and control the wheelchair
            if "forward" in command:
                print("Moving forward")
                speak("Moving forward")  # Read out the command

                # Add code to move the wheelchair forward
            elif "backward" in command:
                print("Moving backward")
                speak("Moving backward")
                # Add code to move the wheelchair backward
            elif "left" in command:
                print("Turning left")
                speak("Turning left")
                # Add code to turn the wheelchair left
            elif "right" in command:
                print("Turning right")
                speak("Turning right")
                # Add code to turn the wheelchair right
            elif "stop" in command:
                print("Stopping")
                speak("Stopping")
                # Add code to stop the wheelchair
            elif "exit" in command:
                print("Exiting voice control")
                speak("Exiting voice control")
                break
            else:
                print("Unknown command")
                speak("Unknown command")
