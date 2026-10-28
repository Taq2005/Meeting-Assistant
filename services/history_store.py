"""Persistent local storage for generated meeting reports."""
from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import List

from core.models import ActionItem, MeetingContext, MeetingMinutes, MeetingResult

HISTORY_DB_PATH = Path(__file__).resolve().parents[1] / "meeting_history.db"


@dataclass
class SavedMeeting:
    id: int
    created_at: str
    result: MeetingResult


def _ensure_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            result_json TEXT NOT NULL
        )
        """
    )


def save_meeting(
    result: MeetingResult, database_path: Path = HISTORY_DB_PATH
) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            _ensure_schema(connection)
            connection.execute(
                "INSERT INTO meetings (created_at, result_json) VALUES (?, ?)",
                (
                    datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    json.dumps(asdict(result), ensure_ascii=False),
                ),
            )


def _deserialize_result(result_json: str) -> MeetingResult:
    data = json.loads(result_json)
    minutes_data = data["minutes"]
    return MeetingResult(
        context=MeetingContext(**data["context"]),
        transcript=data["transcript"],
        summary=data["summary"],
        minutes=MeetingMinutes(
            attendees=minutes_data["attendees"],
            agenda_items=minutes_data["agenda_items"],
            discussion=minutes_data["discussion"],
            decisions=minutes_data["decisions"],
            action_items=[
                ActionItem(**action_item)
                for action_item in minutes_data["action_items"]
            ],
        ),
        key_points=data["key_points"],
        recommendations=data["recommendations"],
    )


def load_meetings(database_path: Path = HISTORY_DB_PATH) -> List[SavedMeeting]:
    if not database_path.exists():
        return []

    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            _ensure_schema(connection)
            rows = connection.execute(
                "SELECT id, created_at, result_json FROM meetings ORDER BY id DESC"
            ).fetchall()
    return [
        SavedMeeting(
            id=meeting_id,
            created_at=created_at,
            result=_deserialize_result(result_json),
        )
        for meeting_id, created_at, result_json in rows
    ]
