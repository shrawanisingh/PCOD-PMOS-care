from services.llm_service import ask_llm
from prompts.lifestyle_prompt import LIFESTYLE_PROMPT

def run_lifestyle(user_input):

    return ask_llm(
        LIFESTYLE_PROMPT,
        user_input
    )