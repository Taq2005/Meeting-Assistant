"""Coordinates transcription and the four analysis agents."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Optional

from agents.key_points import KeyPointsAgent
from agents.minutes import MinutesAgent
from agents.recommendations import RecommendationsAgent
from agents.summarizer import SummarizerAgent
from core.gemini_client import GeminiClient
from core.models import MeetingContext, MeetingResult
from services.audio_processor import transcribe_audio

ProgressCallback = Callable[[float, str], None]

LABELS = {
    "summary": "summary",
    "minutes": "minutes",
    "key_points": "key points",
    "recommendations": "recommendations",
}


class MeetingOrchestrator:
    def __init__(self, client: GeminiClient):
        self.client = client
        self.agents = {
            agent.name: agent
            for agent in (
                SummarizerAgent(client),
                MinutesAgent(client),
                KeyPointsAgent(client),
                RecommendationsAgent(client),
            )
        }

    def process(self, audio_bytes: bytes, filename: str, context: MeetingContext,
                progress: Optional[ProgressCallback] = None) -> MeetingResult:
        def report(fraction: float, message: str) -> None:
            if progress:
                progress(min(fraction, 1.0), message)

        report(0.05, "Uploading and transcribing audio...")
        transcript = transcribe_audio(self.client, audio_bytes, filename, context)

        report(0.40, "Analysing the meeting...")
        results = {}
        # Agents run in parallel; progress is reported from this (main) thread.
        with ThreadPoolExecutor(max_workers=len(self.agents)) as pool:
            futures = {pool.submit(agent.run, transcript, context): name
                       for name, agent in self.agents.items()}
            for done, future in enumerate(as_completed(futures), start=1):
                name = futures[future]
                results[name] = future.result()
                report(0.40 + 0.60 * done / len(futures), f"Finished {LABELS[name]}")

        return MeetingResult(
            context=context,
            transcript=transcript,
            summary=results["summary"],
            minutes=results["minutes"],
            key_points=results["key_points"],
            recommendations=results["recommendations"],
        )
