"""Produces formal meeting minutes."""
from agents.base import BaseAgent
from core.models import ActionItem, MeetingMinutes
from core.prompts import MINUTES_PROMPT


def _as_list(value) -> list:
    return [str(v).strip() for v in value if str(v).strip()] if isinstance(value, list) else []


class MinutesAgent(BaseAgent):
    name = "minutes"
    prompt_template = MINUTES_PROMPT

    def parse(self, data) -> MeetingMinutes:
        actions = []
        for item in data.get("action_items", []) or []:
            if isinstance(item, dict) and item.get("task"):
                actions.append(ActionItem(
                    task=str(item["task"]).strip(),
                    owner=str(item.get("owner") or "Not specified").strip(),
                    due=str(item.get("due") or "Not specified").strip(),
                ))
        return MeetingMinutes(
            attendees=_as_list(data.get("attendees")),
            agenda_items=_as_list(data.get("agenda_items")),
            discussion=_as_list(data.get("discussion")),
            decisions=_as_list(data.get("decisions")),
            action_items=actions,
        )
