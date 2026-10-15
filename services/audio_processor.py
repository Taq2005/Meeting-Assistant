"""Turns an audio recording into a speaker-labelled transcript."""
import os
import tempfile
from pathlib import Path

from core.config.settings import AUDIO_MIME_TYPES
from core.gemini_client import GeminiClient, GeminiError
from core.models import MeetingContext
from core.prompts import SYSTEM_INSTRUCTION, TRANSCRIPTION_PROMPT, render


def transcribe_audio(client: GeminiClient, audio_bytes: bytes, filename: str,
                     context: MeetingContext) -> str:
    suffix = Path(filename).suffix.lower().lstrip(".")
    mime_type = AUDIO_MIME_TYPES.get(suffix)
    if not mime_type:
        raise GeminiError(f"Unsupported audio format: .{suffix}")

    tmp_path = None
    uploaded = None
    try:
        with tempfile.NamedTemporaryFile(suffix=f".{suffix}", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        uploaded = client.upload_audio(tmp_path, mime_type)
        prompt = render(TRANSCRIPTION_PROMPT, context=context.as_text())
        return client.generate_text([prompt, uploaded], SYSTEM_INSTRUCTION).strip()
    finally:
        if uploaded is not None:
            client.delete_file(uploaded)
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
