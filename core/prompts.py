"""All prompt templates live here, separate from application logic."""

SYSTEM_INSTRUCTION = (
    "You are an expert meeting analyst. Work only from the meeting transcript provided. "
    "Do not invent facts, names, dates or decisions. If something is not stated, write "
    "'Not specified'. Write in clear, professional English."
)


def render(template: str, **values: str) -> str:
    """Fill {placeholders} without clashing with JSON braces in the templates."""
    out = template
    for key, value in values.items():
        out = out.replace("{" + key + "}", value)
    return out


TRANSCRIPTION_PROMPT = """Transcribe the attached meeting audio accurately in English.

Requirements:
- Label speakers consistently as Speaker 1, Speaker 2, and so on, one turn per line.
  If a speaker's name is clearly stated in the audio, use that name instead.
- Start each turn with a [MM:SS] timestamp.
- Do not summarise or leave out content.
- Mark unclear audio as [inaudible].

Meeting context (use it to spell names and terms correctly):
{context}

Return only the transcript, with no introduction or commentary."""


SUMMARY_PROMPT = """Write an executive summary of the meeting below.

Meeting context:
{context}

Transcript:
{transcript}

Return JSON with exactly this shape:
{"summary": "A concise summary of 120-200 words covering purpose, main topics, outcomes and next steps."}"""


MINUTES_PROMPT = """Prepare formal minutes of the meeting below.

Meeting context:
{context}

Transcript:
{transcript}

Return JSON with exactly this shape:
{
  "attendees": ["names, or Speaker labels if names are unknown"],
  "agenda_items": ["agenda topics actually covered"],
  "discussion": ["one concise paragraph per topic discussed, in the order discussed"],
  "decisions": ["each decision that was made"],
  "action_items": [{"task": "what must be done", "owner": "who", "due": "when"}]
}
Use "Not specified" for any owner or due date that was not stated."""


KEY_POINTS_PROMPT = """Extract the key points discussed in the meeting below.

Meeting context:
{context}

Transcript:
{transcript}

Return JSON with exactly this shape:
{"key_points": ["6-10 short, specific points, most important first"]}"""


RECOMMENDATIONS_PROMPT = """Based on the meeting below, give practical recommendations and next steps.
Ground each one in something that was discussed, such as risks raised, open questions,
unresolved disagreements or missed deadlines.

Meeting context:
{context}

Transcript:
{transcript}

Return JSON with exactly this shape:
{"recommendations": ["3-8 clear, actionable recommendations"]}"""
