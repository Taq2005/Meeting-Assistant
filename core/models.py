"""Data models shared across the application."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class MeetingContext:
    """Details supplied by the user to improve transcription and analysis."""

    title: str = ""
    date: str = ""
    agenda: str = ""
    glossary: str = ""

    def as_text(self) -> str:
        def val(v: str) -> str:
            return v.strip() if v and v.strip() else "Not provided"

        return (
            f"Title: {val(self.title)}\n"
            f"Date: {val(self.date)}\n"
            f"Agenda: {val(self.agenda)}\n"
            f"Glossary / background: {val(self.glossary)}"
        )


@dataclass
class ActionItem:
    task: str = ""
    owner: str = "Not specified"
    due: str = "Not specified"


@dataclass
class MeetingMinutes:
    attendees: List[str] = field(default_factory=list)
    agenda_items: List[str] = field(default_factory=list)
    discussion: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)


@dataclass
class MeetingResult:
    context: MeetingContext
    transcript: str
    summary: str
    minutes: MeetingMinutes
    key_points: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
