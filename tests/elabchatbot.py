from dotenv import load_dotenv
load_dotenv()
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(
  api_key=ELEVENLABS_API_KEY, # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

audio = client.generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice="Emily",
  model="eleven_multilingual_v2"
)
play(audio)