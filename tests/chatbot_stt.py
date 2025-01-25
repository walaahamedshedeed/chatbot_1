from RealtimeSTT import AudioToTextRecorder
import time
from dotenv import load_dotenv
load_dotenv()

from elevenlabs import play
from elevenlabs.client import ElevenLabs
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(
  api_key=ELEVENLABS_API_KEY, # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

def process_text(text):
    print(text)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(language="en")

    while True:
        text = recorder.text()
        print(text)
        audio = client.generate(
            text=text,
            voice="Mark - Natural Conversations",
            model="eleven_flash_v2_5",
            # stream=True
        )
        play(audio)
        time.sleep(5)