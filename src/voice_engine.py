from pathlib import Path
from gtts import gTTS
from utils import play_sound
import subprocess 
import os
import vosk
import pyaudio
import pygame
import json
import speech_recognition as sr
import time
from gpiozero import Button

pygame.mixer.init()

MIC_INDEX = 1
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "lang_model"

model = vosk.Model(str(MODEL_PATH))
# vosk only listens for these sounds, increasing accuracy and performance
grammer = '["hey pie", "hey pi", "[unk]"]' 

mute_switch = Button(17, pull_up=True)

# text to speech
def speak(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("response.mp3")

        print(f"Response: {text}")
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.unload()
        os.remove("response.mp3")
    except Exception as e:
        print(f"Audio Error: {e}")


# speech to text
def listen():

    if mute_switch.is_pressed:
        return 'Mic is muted.'
    
    recognizer = sr.Recognizer()

    # open the desired microphone
    with sr.Microphone(device_index=MIC_INDEX) as source:
        print("Listening for your prompt...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        if mute_switch.is_pressed:
            return 'Mic is muted.'
        
        try:
            # listening for input
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("No speech was detected before timeout.")
            return None
        
    try:
        # convert raw audio data to text
        text = recognizer.recognize_google(audio)
        text = text.lower()
        print(f"Prompt: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech was uncleaer. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition failed. Error: {e}")
        return None
    

def wake_word():
    wake_recognizer = vosk.KaldiRecognizer(model, 48000, grammer)
    p = pyaudio.PyAudio()

    print("\nWake word detection online. Waiting to hear 'Hey Pi'...")

    try:
        play_sound("prompt_sound.mp3")
    except pygame.error as e:
        print(f"Pygame Error: {e}")
    except FileNotFoundError:
        print("Sound file not found, skipping chime.")

    while True:

        if mute_switch.is_pressed:
            print("Mic is muted.")
            time.sleep(1)
            continue

        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=48000,
            input=True,
            input_device_index=MIC_INDEX,
            frames_per_buffer=8000
        )

        try:
            wake_detected = False
            while True:

                if mute_switch.is_pressed:
                    print("\nMic is muted.")
                    break

                data = stream.read(4000, exception_on_overflow=False)
                if wake_recognizer.AcceptWaveform(data):
                    result = json.loads(wake_recognizer.Result())
                    text = result.get("text", "")

                    # checking custom wake word
                    if "hey pie" in text or "hey pi" in text:
                        print(f"\nWake word detected. (Vosk heard: Hey Pi)")
                        wake_detected = True
                        break
        finally:
            stream.stop_stream()
            stream.close()
        
        if wake_detected:
            speak("Yes?")
            return