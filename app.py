"""Streamlit entry point. Run with:  streamlit run app.py"""
import streamlit as st

from agents.orchestrator import MeetingOrchestrator
from core.config.settings import APP_TITLE, MAX_AUDIO_MB
from core.gemini_client import GeminiClient, GeminiError
from ui.components import (render_downloads, render_header, render_input_form,
                           render_results, render_sidebar)
from ui.theme import apply_theme

st.set_page_config(page_title=APP_TITLE, layout="wide")
apply_theme()
render_header()

api_key, model = render_sidebar()
context, audio_file, submitted = render_input_form()

if submitted:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif audio_file is None:
        st.warning("Please upload an audio recording.")
    elif audio_file.size > MAX_AUDIO_MB * 1024 * 1024:
        st.error(f"The file is larger than {MAX_AUDIO_MB} MB.")
    else:
        bar = st.progress(0.0, text="Starting...")
        try:
            orchestrator = MeetingOrchestrator(GeminiClient(api_key, model))

            def report_progress(fraction: float, message: str) -> None:
                bar.progress(fraction, text=message)

            result = orchestrator.process(
                audio_file.getvalue(), audio_file.name, context,
                progress=report_progress,
            )
            st.session_state["result"] = result
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
