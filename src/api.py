import os
from google import genai
from dotenv import load_dotenv

class APIEngine:
    def __init__(self):
        # load environment variable (MY_API_KEY)
        load_dotenv()
        self.api_key = os.getenv("MY_API_KEY")

        if not self.api_key:
            raise ValueError("MY_API_KEY is not set. Please check your.env file.")
        
        # initializing client and chat session
        self.client = genai.Client(api_key=self.api_key)
        self.chat = self.client.chats.create(model="gemini-3-flash-preview")

    def ask(self, prompt, image_path=None):
        try:
            if image_path and os.path.exists(image_path):
                uploaded_image = self.client.files.upload(file=image_path)
                response = self.chat.send_message([prompt, uploaded_image])
            else:
                response = self.chat.send_message(prompt)

            return response.text
        except Exception as e:
            print(f"API Error: {e}")
            return "Failed to connect to API."