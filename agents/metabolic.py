from services.llm_service import ask_llm
from prompts.metabolic_prompt import METABOLIC_PROMPT

def run_metabolic(user_input):

    return ask_llm(
        METABOLIC_PROMPT,
        user_input
    )