"""Shared behaviour for all analysis agents."""
from typing import Any

from core.gemini_client import GeminiClient
from core.models import MeetingContext
from core.prompts import SYSTEM_INSTRUCTION, render


class BaseAgent:
    """Subclasses set `name` and `prompt_template` and implement `parse`."""

    name = "base"
    prompt_template = ""

    def __init__(self, client: GeminiClient):
        self.client = client

    def run(self, transcript: str, context: MeetingContext) -> Any:
        prompt = render(self.prompt_template,
                        context=context.as_text(), transcript=transcript)
        data = self.client.generate_json(prompt, SYSTEM_INSTRUCTION)
        return self.parse(data)

    def parse(self, data: Any) -> Any:
        raise NotImplementedError
