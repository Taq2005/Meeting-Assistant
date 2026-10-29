"""Visual theme for the Streamlit interface."""
import streamlit as st

_TOKENS = {
    "__PAPER__": "#F3F5F1",
    "__INK__": "#1D2B27",
    "__MUTED__": "#5B6B65",
    "__RULE__": "#CBD5CF",
    "__PINE__": "#0E5A4B",
    "__PINE_DARK__": "#0A4237",
    "__PINE_TINT__": "#DDEBE5",
    "__MARKER__": "#F2C94C",
    "__MARKER_TINT__": "#FBF0BF",
}

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
    --paper: __PAPER__;
    --ink: __INK__;
    --muted: __MUTED__;
    --rule: __RULE__;
    --pine: __PINE__;
    --pine-dark: __PINE_DARK__;
    --pine-tint: __PINE_TINT__;
    --marker: __MARKER__;
    --marker-tint: __MARKER_TINT__;
    --serif: 'Fraunces', Georgia, 'Times New Roman', serif;
    --sans: 'Instrument Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

.stApp { background-color: var(--paper); color: var(--ink); }
.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea,
.stApp button, .stApp td, .stApp th { font-family: var(--sans); }

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stHeaderActionElements"],
#MainMenu, footer { display: none; }

.block-container { max-width: 1040px; padding: 2.6rem 2rem 4rem; }

.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: var(--serif);
    color: var(--ink);
    font-weight: 600;
    letter-spacing: -0.01em;
}

.stApp .masthead { margin-bottom: 2rem; }
.stApp .masthead h1 {
    font-size: 2.7rem;
    line-height: 1.1;
    margin: 0;
    padding: 0;
}
.stApp .masthead p {
    color: var(--muted);
    font-size: 1.05rem;
    margin: 0.6rem 0 1.1rem 0;
    max-width: 52ch;
}
.stApp .masthead::after {
    content: "";
    display: block;
    height: 3px;
    background: linear-gradient(90deg, var(--marker) 0 5rem, var(--pine) 5rem 100%);
}

.stTabs [data-baseweb="tab-list"] { gap: 0.4rem; }
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: var(--muted);
    padding: 0.7rem 1.1rem;
    font-weight: 500;
}
.stTabs [data-baseweb="tab"] p { font-size: 1rem; }
.stTabs [aria-selected="true"] { color: var(--pine); }
.stTabs [aria-selected="true"] p { font-weight: 600; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--pine); height: 3px; }
.stTabs [data-baseweb="tab-border"] { background-color: var(--rule); }

[data-testid="stForm"] {
    background-color: #FFFFFF;
    border: 1px solid var(--rule);
    border-radius: 10px;
    padding: 1.6rem 1.8rem;
}

[data-testid="stWidgetLabel"] p {
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--ink);
}

[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid var(--rule) !important;
    border-radius: 6px !important;
}
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: var(--pine) !important;
    box-shadow: 0 0 0 1px var(--pine) !important;
}
.stApp input, .stApp textarea { color: var(--ink); }
.stApp input::placeholder, .stApp textarea::placeholder {
    color: #5E706A;
    opacity: 1;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #FFFFFF;
    border: 1.5px dashed var(--pine);
    border-radius: 8px;
    padding: 1.1rem 1.2rem;
}

.stButton > button, .stFormSubmitButton > button {
    background-color: var(--pine);
    color: #FFFFFF;
    border: 1.5px solid var(--pine);
    border-radius: 6px;
    padding: 0.65rem 1.6rem;
    font-weight: 600;
    font-size: 1rem;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: var(--pine-dark);
    border-color: var(--pine-dark);
    color: #FFFFFF;
}

.stDownloadButton > button {
    background-color: transparent;
    color: var(--pine);
    border: 1.5px solid var(--pine);
    border-radius: 6px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
}
.stDownloadButton > button:hover {
    background-color: var(--pine);
    border-color: var(--pine);
    color: #FFFFFF;
}
.stApp button:focus-visible { outline: 2px solid var(--pine); outline-offset: 2px; }

.stTabs [data-testid="stMarkdownContainer"] p,
.stTabs [data-testid="stMarkdownContainer"] li {
    max-width: 72ch;
    line-height: 1.7;
}
.stTabs [data-testid="stMarkdownContainer"] li::marker { color: var(--pine); }
.stTabs [data-testid="stMarkdownContainer"] h3 {
    font-size: 1.3rem;
    margin-top: 1.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--rule);
}

.summary {
    font-family: var(--serif);
    font-size: 1.12rem;
    line-height: 1.75;
    color: var(--ink);
    max-width: 68ch;
    border-left: 4px solid var(--marker);
    padding: 0.2rem 0 0.2rem 1.3rem;
    margin: 0.8rem 0 1rem 0;
}

.actions-wrap { overflow-x: auto; margin-bottom: 0.8rem; }
.actions { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
.actions th {
    text-align: left;
    font-weight: 600;
    color: var(--muted);
    padding: 0.5rem 0.7rem;
    border-bottom: 2px solid var(--ink);
}
.actions td {
    padding: 0.75rem 0.7rem;
    vertical-align: top;
    border-bottom: 1px solid var(--rule);
    line-height: 1.5;
}
.actions th:nth-child(1), .actions td:nth-child(1) { width: 62%; }
.actions th:nth-child(2), .actions td:nth-child(2),
.actions th:nth-child(3), .actions td:nth-child(3) { width: 19%; }
.chip {
    display: inline-block;
    padding: 0.1rem 0.7rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.88rem;
}
.chip.owner { background-color: var(--pine-tint); color: var(--pine); }
.chip.due { background-color: var(--marker-tint); color: var(--ink); }

.transcript {
    max-height: 450px;
    overflow-y: auto;
    background-color: #FFFFFF;
    border: 1px solid var(--rule);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    font-size: 0.95rem;
    line-height: 1.65;
}
.tline {
    display: grid;
    grid-template-columns: 3.6rem 7.5rem 1fr;
    gap: 0.8rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid #EAEFEB;
}
.tline:last-child { border-bottom: none; }
.tline.plain { display: block; }
.tline .ts {
    color: var(--muted);
    font-size: 0.85rem;
    font-variant-numeric: tabular-nums;
    padding-top: 0.1rem;
}
.tline .spk { font-weight: 600; color: var(--pine); }

[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid var(--rule);
    border-radius: 8px;
}
[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid var(--rule);
    border-radius: 8px;
}

@media (max-width: 640px) {
    .block-container { padding: 1.5rem 1rem 3rem; }
    .stApp .masthead h1 { font-size: 2rem; }
    .tline { grid-template-columns: 1fr; gap: 0.1rem; }
    .summary { font-size: 1.05rem; }
}
</style>
"""


def apply_theme() -> None:
    css = _CSS
    for token, value in _TOKENS.items():
        css = css.replace(token, value)
    st.markdown(css, unsafe_allow_html=True)