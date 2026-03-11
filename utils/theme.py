import streamlit as st

# -----------------------------
# Personnalisation du thème
# -----------------------------
def load_css():
    st.markdown("""
    <style>

    /* PAGE BACKGROUND */
    .stApp {
        background-color: white;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #000A2E;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] a:hover {
        color: #ff7a00;
    }

    /* FILTERS BORDER */

    div[data-baseweb="select"] > div {
        border: 2px solid #ff7a00;
        border-radius: 8px;
    }

    div[data-baseweb="tag"] {
        background-color: #ff7a00 !important;
        color: white !important;
    }

    div[data-testid="stSlider"] > div {
        border: 2px solid #ff7a00;
        border-radius: 8px;
        padding: 6px;
    }

    </style>
    """, unsafe_allow_html=True)

def kpi_card(title, value, delta=None, icon=""):

    delta_html = ""
    if delta:
        delta_html = f"<p style='color:#ff7a00;font-size:14px;margin:0'>{delta}</p>"

    st.markdown(
        f"""
        <div style="
            background:white;
            padding:20px;
            border-radius:12px;
            border:1px solid #e6e6e6;
            box-shadow:0 4px 10px rgba(0,0,0,0.05);
        ">
            <div style="font-size:14px;color:gray">{icon} {title}</div>
            <div style="font-size:32px;font-weight:700">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )