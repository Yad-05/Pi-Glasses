from pathlib import Path
import pygame

BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "assets" / "audio"

pygame.mixer.init()

def play_sound(filename):
    sound_path = AUDIO_DIR / filename
    if sound_path.exists():
        pygame.mixer.music.load(str(sound_path))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)