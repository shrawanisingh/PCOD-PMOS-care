from services.llm_service import ask_llm
from prompts.clinical_prompt import CLINICAL_PROMPT

def run_clinical(user_input):

    return ask_llm(
        CLINICAL_PROMPT,
        user_input
    )