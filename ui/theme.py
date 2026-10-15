"""Blue and white theme for the Streamlit interface."""
import streamlit as st

BLUE = "#1E5BD8"
DARK_BLUE = "#123C8F"
LIGHT_BLUE = "#EAF1FD"
BORDER_BLUE = "#B8CCF2"

_CSS = """
<style>
.stApp { background-color: #FFFFFF; }

.app-header {
    background: linear-gradient(90deg, __DARK__ 0%, __BLUE__ 100%);
    color: #FFFFFF;
    padding: 1.4rem 1.8rem;
    border-radius: 12px;
    margin-bottom: 1.4rem;
}
.app-header h1 { color: #FFFFFF; margin: 0; font-size: 1.9rem; }
.app-header p  { color: #DCE7FB; margin: 0.3rem 0 0 0; }

[data-testid="stSidebar"] { background-color: __LIGHT__; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] label { color: __DARK__; }

h2, h3 { color: __DARK__; }

.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    background-color: __BLUE__;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
}
.stButton > button:hover, .stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background-color: __DARK__;
    color: #FFFFFF;
}

.stTabs [data-baseweb="tab-list"] { gap: 6px; }
.stTabs [data-baseweb="tab"] {
    background-color: __LIGHT__;
    border-radius: 8px 8px 0 0;
    color: __DARK__;
    padding: 0.5rem 1rem;
}
.stTabs [aria-selected="true"] { background-color: __BLUE__; color: #FFFFFF; }

.card {
    background-color: __LIGHT__;
    border: 1px solid __BORDER__;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    color: #0F2A5C;
}
</style>
"""


def apply_theme() -> None:
    css = (_CSS.replace("__BLUE__", BLUE).replace("__DARK__", DARK_BLUE)
           .replace("__LIGHT__", LIGHT_BLUE).replace("__BORDER__", BORDER_BLUE))
    st.markdown(css, unsafe_allow_html=True)
