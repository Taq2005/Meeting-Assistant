"""Produces recommendations and next steps."""
from agents.base import BaseAgent
from core.prompts import RECOMMENDATIONS_PROMPT


class RecommendationsAgent(BaseAgent):
    name = "recommendations"
    prompt_template = RECOMMENDATIONS_PROMPT

    def parse(self, data) -> list:
        recs = data.get("recommendations", [])
        return [str(r).strip() for r in recs if str(r).strip()] if isinstance(recs, list) else []
