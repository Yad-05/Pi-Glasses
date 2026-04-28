from pathlib import Path
import subprocess
import datetime

def capture():
    base_dir = Path(__file__).resolve().parent.parent
    images_dir = base_dir / "captured_images"

    # creates the images directory if not already available
    images_dir.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = images_dir / f"{timestamp}_captured_image.jpg"

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
        print("Fialed to capture image with 'rpicam-jepg'.")
        return None
    except FileNotFoundError:
        print("System Error: 'rpicam-jpeg' command not found. If you're running on Raspberry Pi, Please install 'rpicam-jpeg' by running: \n" \
        "sudo apt full-upgrade\n" \
        "sudo apt install -y libcamera-apps")
        return None