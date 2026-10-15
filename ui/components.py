"""Reusable Streamlit components."""
from html import escape
from typing import Optional, Tuple

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from core.config.settings import (ALLOWED_AUDIO_TYPES, APP_TITLE, AVAILABLE_MODELS,
                             get_env_api_key)
from core.models import MeetingContext, MeetingResult
from services.exporter import to_docx, to_pdf


def render_header() -> None:
    st.markdown(
        f'<div class="app-header"><h1>{APP_TITLE}</h1>'
        "<p>Upload a meeting recording to get a summary, minutes, key points "
        "and recommendations.</p></div>",
        unsafe_allow_html=True,
    )


def render_sidebar() -> Tuple[str, str]:
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("Gemini API key", type="password",
                                value=get_env_api_key(),
                                help="Or set GEMINI_API_KEY in a .env file.")
        model = st.selectbox("Model", AVAILABLE_MODELS, index=0)
        st.caption("Your key is used only for this session and is never stored.")
    return api_key, model


def render_input_form() -> Tuple[MeetingContext, Optional[UploadedFile], bool]:
    with st.form("meeting_form"):
        st.subheader("1. Meeting details")
        col1, col2 = st.columns([2, 1])
        title = col1.text_input("Meeting title")
        date = col2.text_input("Date", placeholder="e.g. 15 Oct 2026")
        agenda = st.text_area("Agenda", height=100,
                              placeholder="One topic per line (optional)")
        glossary = st.text_area("Glossary and background", height=100,
                                placeholder="Project names, acronyms, people and terms "
                                            "(helps transcription accuracy)")
        st.subheader("2. Audio recording")
        audio_file = st.file_uploader("Upload audio", type=ALLOWED_AUDIO_TYPES)
        submitted = st.form_submit_button("Generate meeting report")
    context = MeetingContext(title=title, date=date, agenda=agenda, glossary=glossary)
    return context, audio_file, submitted


def _bullets(items) -> None:
    if not items:
        st.write("Not specified.")
        return
    for item in items:
        st.markdown(f"- {item}")


def render_downloads(result: MeetingResult) -> None:
    st.subheader("Download report")
    col1, col2, _ = st.columns([1, 1, 2])
    col1.download_button(
        "Download DOCX", data=to_docx(result), file_name="meeting_report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    col2.download_button(
        "Download PDF", data=to_pdf(result), file_name="meeting_report.pdf",
        mime="application/pdf")


def render_results(result: MeetingResult) -> None:
    tabs = st.tabs(["Summary", "Minutes", "Key Points", "Recommendations", "Transcript"])

    with tabs[0]:
        st.markdown(f'<div class="card">{escape(result.summary)}</div>',
                    unsafe_allow_html=True)

    with tabs[1]:
        m = result.minutes
        st.markdown("### Attendees")
        _bullets(m.attendees)
        st.markdown("### Agenda items")
        _bullets(m.agenda_items)
        st.markdown("### Discussion")
        if m.discussion:
            for para in m.discussion:
                st.write(para)
        else:
            st.write("Not specified.")
        st.markdown("### Decisions")
        _bullets(m.decisions)
        st.markdown("### Action items")
        if m.action_items:
            st.dataframe(
                [{"Task": a.task, "Owner": a.owner, "Due": a.due} for a in m.action_items],
                use_container_width=True, hide_index=True)
        else:
            st.write("Not specified.")

    with tabs[2]:
        _bullets(result.key_points)

    with tabs[3]:
        _bullets(result.recommendations)

    with tabs[4]:
        st.text_area("Transcript", result.transcript, height=450,
                     label_visibility="collapsed")
