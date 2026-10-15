"""Produces the executive summary."""
from agents.base import BaseAgent
from core.prompts import SUMMARY_PROMPT


class SummarizerAgent(BaseAgent):
    name = "summary"
    prompt_template = SUMMARY_PROMPT

    def parse(self, data) -> str:
        return str(data.get("summary", "")).strip()
