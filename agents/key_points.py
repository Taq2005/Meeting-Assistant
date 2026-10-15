"""Extracts the key discussion points."""
from agents.base import BaseAgent
from core.prompts import KEY_POINTS_PROMPT


class KeyPointsAgent(BaseAgent):
    name = "key_points"
    prompt_template = KEY_POINTS_PROMPT

    def parse(self, data) -> list:
        points = data.get("key_points", [])
        return [str(p).strip() for p in points if str(p).strip()] if isinstance(points, list) else []
