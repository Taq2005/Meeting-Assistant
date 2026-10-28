"""Reusable Streamlit components."""
from html import escape
from typing import Dict, List, Optional, Tuple

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from core.config.settings import ALLOWED_AUDIO_TYPES, APP_TITLE
from core.gemini_client import GeminiError
from core.models import MeetingContext, MeetingResult
from services.exporter import to_docx, to_pdf
from services.history_store import SavedMeeting
from services.assistant import answer_question


def render_header() -> None:
    st.markdown(
        f'<div class="app-header"><h1>{APP_TITLE}</h1>'
        "<p>Upload a meeting recording to get a summary, minutes, key points "
        "and recommendations.</p></div>",
        unsafe_allow_html=True,
    )


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


def render_downloads(result: MeetingResult, key_prefix: str = "current") -> None:
    st.subheader("Download report")
    col1, col2, _ = st.columns([1, 1, 2])
    col1.download_button(
        "Download DOCX", data=to_docx(result), file_name="meeting_report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        key=f"{key_prefix}-download-docx")
    col2.download_button(
        "Download PDF", data=to_pdf(result), file_name="meeting_report.pdf",
        mime="application/pdf", key=f"{key_prefix}-download-pdf")


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


def render_history(meetings: List[SavedMeeting]) -> None:
    st.subheader("Saved meetings")
    if not meetings:
        st.info("Generated meeting reports will appear here.")
        return

    for meeting in meetings:
        title = meeting.result.context.title.strip() or "Untitled meeting"
        date = meeting.result.context.date.strip()
        label = f"{title} - {date}" if date else title
        with st.expander(f"{label} · {meeting.created_at} · #{meeting.id}"):
            result = meeting.result
            render_downloads(result, key_prefix=f"history-{meeting.id}")
            st.markdown("### Summary")
            st.markdown(f'<div class="card">{escape(result.summary)}</div>',
                        unsafe_allow_html=True)
            st.markdown("### Minutes")
            minutes = result.minutes
            st.markdown("#### Attendees")
            _bullets(minutes.attendees)
            st.markdown("#### Agenda items")
            _bullets(minutes.agenda_items)
            st.markdown("#### Discussion")
            if minutes.discussion:
                for paragraph in minutes.discussion:
                    st.write(paragraph)
            else:
                st.write("Not specified.")
            st.markdown("#### Decisions")
            _bullets(minutes.decisions)
            st.markdown("#### Action items")
            if minutes.action_items:
                st.dataframe(
                    [{"Task": item.task, "Owner": item.owner, "Due": item.due}
                     for item in minutes.action_items],
                    use_container_width=True, hide_index=True,
                    key=f"history-{meeting.id}-action-items")
            else:
                st.write("Not specified.")
            st.markdown("### Key points")
            _bullets(result.key_points)
            st.markdown("### Recommendations")
            _bullets(result.recommendations)
            st.markdown("### Transcript")
            st.text(result.transcript)


def render_assistant(meetings: List[SavedMeeting], api_key: str, model: str) -> None:
    st.subheader("App and meeting help")
    meeting_options: Dict[Optional[int], str] = {None: "General app help"}
    for meeting in meetings:
        title = meeting.result.context.title.strip() or "Untitled meeting"
        date = meeting.result.context.date.strip()
        label = f"{title} - {date}" if date else title
        meeting_options[meeting.id] = f"{label} · {meeting.created_at}"

    selected_id = st.selectbox(
        "What should the assistant help with?",
        options=list(meeting_options),
        format_func=lambda meeting_id: meeting_options[meeting_id],
        key="assistant_meeting_selection",
    )
    st.caption(
        "Choose a saved meeting for questions about its summary and minutes, "
        "or choose general help to learn how to use the app."
    )

    threads = st.session_state.setdefault("assistant_threads", {})
    thread_key = "general" if selected_id is None else str(selected_id)
    conversation = threads.setdefault(thread_key, [])

    for message in conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask about the app or selected meeting")
    if question:
        if not api_key:
            st.error(
                "Set the GEMINI_CHATBOT_API_KEY environment variable or add it to your "
                ".env file "
                "to use the assistant."
            )
            return

        conversation.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        try:
            selected_meeting = next(
                (meeting for meeting in meetings if meeting.id == selected_id), None
            )
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = answer_question(
                        question,
                        api_key,
                        conversation[:-1],
                        meeting=selected_meeting.result if selected_meeting else None,
                        model=model,
                    )
                st.markdown(response)
            conversation.append({"role": "assistant", "content": response})
        except GeminiError as exc:
            st.error(f"Could not get an assistant response: {exc}")
