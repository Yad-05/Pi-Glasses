import subprocess
from utils import play_sound
from camera import capture
from voice_engine import speak, listen, wake_word
from api import APIEngine


def main():
    ai = APIEngine()

    camera_triggers = [
        "what's in front of me",
        "what is in front of me",
        "explain this",
        "solve this",
        "what am i holding",
        "what am i looking at"
    ]

    print("\nPi Glasses Boot Sequence Complete")
    play_sound("startup_sound_1.mp3")

    while True:
        wake_word()

        user_input = listen()
        play_sound("prompt_sound.mp3")

        if user_input == 'Mic is muted.':
            print(user_input)
            speak(user_input)
            continue

        if user_input is None:
            response = "Didn't catch that, please repeat."
            speak(response)
            continue
        
        if user_input == "quit":
            speak("Goodbye. Have a great day.")
            play_sound("power_off_sound.mp3")
            break

        if user_input == "shut down":
            speak("Shutting down Pie Glasses.")
            play_sound("power_off_sound.mp3")
            try:
                subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to shut down: {e}")
            break

        final_prompt = user_input.lower()

        needs_camera = any(phrase in user_input for phrase in camera_triggers)

        if needs_camera:
            print("Camera trigger detected. Accessing camera...")
            image_path = capture()
            if image_path:
                response = ai.ask(final_prompt, image_path)
            else:
                response = "I'm sorry, I failed to capture an image"
        else:
            response = ai.ask(final_prompt)

        speak(response)

if __name__ == "__main__":
    main()