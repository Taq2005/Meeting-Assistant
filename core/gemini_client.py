"""Thin wrapper around the Google Gemini API.

This is the only module that knows about the Gemini SDK, so switching model
or provider later is a one-file change.
"""
import json
import time
from typing import Any, List, Optional

from google import genai

from google.genai import types

from core.config.settings import MAX_RETRIES, TEMPERATURE


class GeminiError(Exception):
    """Raised for any failure when talking to Gemini."""


def _parse_json(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise GeminiError(f"Model returned invalid JSON: {exc}") from exc


class GeminiClient:
    def __init__(self, api_key: str, model: str, max_retries: int = MAX_RETRIES):
        if not api_key:
            raise GeminiError("A Gemini API key is required.")
        self._client = genai.Client(api_key=api_key)
        self.model = model
        self.max_retries = max_retries

    # ---- files -------------------------------------------------------
    def upload_audio(self, path: str, mime_type: str):
        """Upload an audio file and wait until Gemini has processed it."""
        try:
            uploaded = self._client.files.upload(
                file=path, config=types.UploadFileConfig(mime_type=mime_type)
            )

            while uploaded.state and uploaded.state.name == "PROCESSING":
                uploaded_name = uploaded.name
                if uploaded_name is None:
                    raise GeminiError("Gemini returned an upload without a file name.")
                time.sleep(2)
                uploaded = self._client.files.get(name=uploaded_name)
            if uploaded.state and uploaded.state.name == "FAILED":
                raise GeminiError("Gemini could not process the audio file.")
            return uploaded
        except GeminiError:
            raise
        except Exception as exc:
            raise GeminiError(f"Audio upload failed: {exc}") from exc

    def delete_file(self, uploaded) -> None:
        try:
            self._client.files.delete(name=uploaded.name)
        except Exception:
            pass  # best-effort cleanup

    # ---- generation --------------------------------------------------
    def _generate(self, contents: List[Any], system_instruction: Optional[str],
                  json_mode: bool) -> str:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=TEMPERATURE,
            response_mime_type="application/json" if json_mode else None,
        )
        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                response = self._client.models.generate_content(
                    model=self.model, contents=contents, config=config
                )
                if not response.text:
                    raise GeminiError("Gemini returned an empty response.")
                return response.text
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
        raise GeminiError(f"Gemini request failed: {last_error}") from last_error

    def generate_text(self, contents: List[Any],
                      system_instruction: Optional[str] = None) -> str:
        return self._generate(contents, system_instruction, json_mode=False)

    def generate_json(self, prompt: str,
                      system_instruction: Optional[str] = None) -> Any:
        return _parse_json(self._generate([prompt], system_instruction, json_mode=True))
