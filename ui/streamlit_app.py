import os
import sys


# Ensure the project root is on the Python path so local imports work when
# running `streamlit run ui/streamlit_app.py` from any directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from graph.workflow import graph

from services.pdf_service import generate_pdf
from services.history_service import (
    save_history,
    get_history
)

st.set_page_config(
    page_title="OvaCare AI",
    page_icon="🩺"
)

st.title("🩺 OvaCare AI")
st.subheader("AI-powered PCOS Care Assistant")
st.sidebar.title("Previous Assessments")

history = get_history()

for item in reversed(history[-5:]):

    with st.sidebar.expander(
        item["query"][:40]
    ):
        st.write(item["report"])

st.markdown("### Patient Information")

age = st.number_input(
    "Age",
    min_value=15,
    max_value=50,
    value=25
)

cycle = st.selectbox(
    "Menstrual Cycle",
    ["Regular", "Irregular", "Absent"]
)

stress = st.selectbox(
    "Stress Level",
    ["Low", "Moderate", "High"]
)

sleep = st.selectbox(
    "Sleep Quality",
    ["Good", "Average", "Poor"]
)

notes = st.text_area(
    "Additional Symptoms",
    placeholder="Acne, hair loss, fatigue, weight gain..."
)

query = f"""
Age: {age}

Menstrual cycle: {cycle}

Stress level: {stress}

Sleep quality: {sleep}

Additional symptoms:
{notes}
"""

mock_mode = st.checkbox("Enable mock LLM mode (useful if GEMINI_API_KEY is unavailable)")
if mock_mode:
    os.environ["MOCK_LLM"] = "1"

if st.button("Analyze"):

    with st.spinner("Analyzing patient profile..."):

        result = graph.invoke(
            {
                "query": query
            }
        )

    report = result.get("final_report", "")

    clinical = result.get(
        "clinical",
        ""
    )

    metabolic = result.get(
        "metabolic",
        ""
    )

    lifestyle = result.get(
        "lifestyle",
        ""
    )

    routing = result.get(
        "routing",
        {}
    )

    st.success("Assessment completed.")

    st.header("Final Report")
    st.markdown(report)

    st.divider()

    st.subheader("Specialist Analysis")

    if clinical:
        with st.expander(
            "🩺 Clinical Specialist"
        ):
            st.markdown(clinical)

    if metabolic:
        with st.expander(
            "🍎 Metabolic Specialist"
        ):
            st.markdown(metabolic)

    if lifestyle:
        with st.expander(
            "🌿 Lifestyle Specialist"
        ):
            st.markdown(lifestyle)

    with st.expander(
        "🤖 Supervisor Decision"
    ):
        st.json(routing)