from gtts import gTTS
import subprocess, os

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