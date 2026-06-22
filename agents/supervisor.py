import json

from services.llm_service import ask_llm
from prompts.supervisor_prompt import SUPERVISOR_PROMPT


def run_supervisor(user_input):

    response = ask_llm(
        SUPERVISOR_PROMPT,
        user_input
    )

    try:
        return json.loads(response)
    except:
        return {
            "clinical": True,
            "metabolic": True,
            "lifestyle": True
        }