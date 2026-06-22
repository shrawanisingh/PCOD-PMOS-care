import os
import sys
import streamlit as st

# Ensure the project root is on the Python path so local imports work when
# running `streamlit run ui/streamlit_app.py` from any directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

    from agents.supervisor import run_supervisor
    from agents.clinical import run_clinical
    from agents.metabolic import run_metabolic
    from agents.lifestyle import run_lifestyle
    from agents.planner import run_planner

    routing = run_supervisor(query)

    st.info(
        f"""
        Selected Specialists:

        Clinical: {routing['clinical']}
        Metabolic: {routing['metabolic']}
        Lifestyle: {routing['lifestyle']}
        """
    )

    clinical = ""
    metabolic = ""
    lifestyle = ""

    if routing["clinical"]:
        with st.spinner("Clinical specialist analyzing..."):
            clinical = run_clinical(query)

    if routing["metabolic"]:
        with st.spinner("Metabolic specialist analyzing..."):
            metabolic = run_metabolic(query)

    if routing["lifestyle"]:
        with st.spinner("Lifestyle specialist analyzing..."):
            lifestyle = run_lifestyle(query)

    combined = f"""
    CLINICAL:
    {clinical}

    METABOLIC:
    {metabolic}

    LIFESTYLE:
    {lifestyle}
    """

    with st.spinner("Generating final report..."):
        report = run_planner(combined)
        save_history(query, report)
        pdf_file = generate_pdf(report)

    st.header("📋 OvaCare Assessment")
    st.markdown(report)

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="Download Report",
            data=file,
            file_name="ovacare_report.pdf",
            mime="application/pdf"
        )
    

    if clinical:
        with st.expander("🩺 Clinical Specialist"):
            st.markdown(clinical)

    if metabolic:
        with st.expander("⚖️ Metabolic Specialist"):
            st.markdown(metabolic)

    if lifestyle:
        with st.expander("🌿 Lifestyle Specialist"):
            st.markdown(lifestyle)

    st.divider()

    st.caption(
        "This information is educational and is not a medical diagnosis."
    )