from services.llm_service import ask_llm
from prompts.planner_prompt import PLANNER_PROMPT

def run_planner(reports):

    return ask_llm(
        PLANNER_PROMPT,
        reports
    )