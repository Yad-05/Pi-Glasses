from pathlib import Path
import subprocess
import datetime

def capture():
    BASE_DIR = Path(__file__).resolve().parent.parent
    IMAGES_DIR = BASE_DIR / "captured_images"

    # creates the images directory if not already available
    IMAGES_DIR.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = IMAGES_DIR / f"{timestamp}_captured_image.jpg"

    try:
        print("Capturing image...")
        # -n (no preview window)
        # -t 1000 (1 second camera warm up time)
        # -o (output file path)
        subprocess.run(
            ["rpicam-jpeg", "-n", "-t", "1000", "-o", str(image_path)],
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL
        )
        print("Image captured.")
        return str(image_path)
    
    except subprocess.CalledProcessError:
        print("Failed to capture image with 'rpicam-jepg'.")
        return None
    except FileNotFoundError:
        print("System Error: 'rpicam-jpeg' command not found. If you're running on Raspberry Pi, Please install 'rpicam-jpeg' by running: \n" \
        "sudo apt full-upgrade\n" \
        "sudo apt install -y libcamera-apps")
        return None