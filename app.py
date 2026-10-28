"""Streamlit entry point. Run with:  streamlit run app.py"""
import sqlite3

import streamlit as st

from agents.orchestrator import MeetingOrchestrator
from core.config.settings import (
    APP_TITLE,
    DEFAULT_MODEL,
    MAX_AUDIO_MB,
    get_chatbot_api_key,
    get_env_api_key,
)
from core.gemini_client import GeminiClient, GeminiError
from services.history_store import load_meetings, save_meeting
from ui.components import (render_assistant, render_downloads, render_header,
                           render_history, render_input_form, render_results)
from ui.theme import apply_theme

st.set_page_config(page_title=APP_TITLE, layout="wide")
apply_theme()
render_header()

meeting_tab, history_tab, assistant_tab = st.tabs(
    ["New meeting", "Meeting history", "Assistant"]
)

with meeting_tab:
    api_key = get_env_api_key()
    context, audio_file, submitted = render_input_form()

    if submitted:
        if not api_key:
            st.error("Set the GEMINI_API_KEY environment variable or add it to your .env file.")
        elif audio_file is None:
            st.warning("Please upload an audio recording.")
        elif audio_file.size > MAX_AUDIO_MB * 1024 * 1024:
            st.error(f"The file is larger than {MAX_AUDIO_MB} MB.")
        else:
            bar = st.progress(0.0, text="Starting...")
            try:
                orchestrator = MeetingOrchestrator(GeminiClient(api_key, DEFAULT_MODEL))

                def report_progress(fraction: float, message: str) -> None:
                    bar.progress(fraction, text=message)

                result = orchestrator.process(
                    audio_file.getvalue(), audio_file.name, context,
                    progress=report_progress,
                )
                st.session_state["result"] = result
                try:
                    save_meeting(result)
                except (OSError, sqlite3.Error) as exc:
                    st.error(f"Report generated, but could not save it: {exc}")
                else:
                    st.success("Meeting report saved to your history.")
            except GeminiError as exc:
                st.error(str(exc))
            except Exception as exc:  # keep the UI alive on unexpected errors
                st.error(f"Unexpected error: {exc}")
            finally:
                bar.empty()

    result = st.session_state.get("result")
    if result:
        render_downloads(result)
        render_results(result)

try:
    saved_meetings = load_meetings()
    history_error = None
except (OSError, sqlite3.Error, ValueError) as exc:
    saved_meetings = []
    history_error = f"Could not load meeting history: {exc}"

with history_tab:
    if history_error:
        st.error(history_error)
    else:
        render_history(saved_meetings)

with assistant_tab:
    if history_error:
        st.error(history_error)
    render_assistant(saved_meetings, get_chatbot_api_key(), DEFAULT_MODEL)
