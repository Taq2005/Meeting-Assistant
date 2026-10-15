"""Central settings for the Meeting Assistant."""
import os

from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "Meeting Assistant"

DEFAULT_MODEL = "gemini-3.5-flash-lite"
AVAILABLE_MODELS = ["gemini-3.5-flash-lite", "gemini-2.5-pro", "gemini-2.5-flash-lite"]

# Extension -> MIME type accepted by the Gemini Files API
AUDIO_MIME_TYPES = {
    "mp3": "audio/mp3",
    "wav": "audio/wav",
    "m4a": "audio/mp4",
    "aac": "audio/aac",
    "ogg": "audio/ogg",
    "flac": "audio/flac",
    "webm": "audio/webm",
}
ALLOWED_AUDIO_TYPES = list(AUDIO_MIME_TYPES.keys())
MAX_AUDIO_MB = 200

MAX_RETRIES = 3
TEMPERATURE = 0.3


def get_env_api_key() -> str:
    """Return the API key from the environment / .env file, if any."""
    return os.getenv("GEMINI_API_KEY", "")
