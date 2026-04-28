from gtts import gTTS
import subprocess, os
import speech_recognition as sr

MIC_INDEX = 1

# text to speech
def speak(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("response.mp3")

        subprocess.run(
            ["mpg123", "-q", "response.mp3"],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
        print(text)
        os.remove("response.mp3")
    except Exception as e:
        print(f"Audio Error: {e}")


# speech to text
def listen():
    recognizer = sr.Recognizer()

    # open the desired microphone
    with sr.Microphone(device_index=MIC_INDEX) as source:
        print("Listening for your prompt...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
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
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech was uncleaer. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition failed. Error: {e}")
        return None