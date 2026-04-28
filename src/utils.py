from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "assets" / "audio"

def play_sound(filename):
    sound_path = AUDIO_DIR / filename
    if sound_path.exists():
        subprocess.run(
            ["mpg123", "-q", str(sound_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )