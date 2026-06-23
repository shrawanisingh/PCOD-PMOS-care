import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MODEL = "gemini-2.5-flash"


def _use_mock() -> bool:
    return os.getenv("MOCK_LLM", "0") == "1"


def _get_client():
    if _use_mock():
        return None

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning(
            "GEMINI_API_KEY not set. Using placeholder response instead of live LLM."
        )
        return None

    return genai.Client(api_key=api_key)


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    """Send a combined prompt to the LLM and return the text output.

    Raises RuntimeError on API failures.
    """

    prompt = f"""
    Follow all instructions exactly.

    {system_prompt}

    Patient Input:
    {user_prompt}
    """

    # Short-circuit to a deterministic mock response when requested.
    if _use_mock():
        logger.info("MOCK_LLM enabled — returning canned response")
        return f"[MOCK] This is a mocked LLM response for input: {user_prompt}"

    client = _get_client()
    if client is None:
        logger.warning("GEMINI client unavailable; returning placeholder response.")
        return (
            "[LLM unavailable. Returning placeholder response for testing. "
            "Set GEMINI_API_KEY or enable MOCK_LLM=1 to avoid this fallback.]"
        )

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=300
            )
        )
    except genai.errors.APIError as e:
        # Handle API quota/rate-limit and service availability errors with a safe fallback.
        msg = str(e)
        status_code = getattr(e, "status_code", None)
        if (
            status_code == 429
            or status_code == 503
            or "RESOURCE_EXHAUSTED" in msg
            or "quota" in msg.lower()
            or "UNAVAILABLE" in msg.upper()
        ):
            logger.warning("LLM unavailable: %s", msg)
            return (
                "[LLM unavailable. Returning placeholder response for testing. "
                "Replace GEMINI_API_KEY, upgrade quota, or retry later.]"
            )
        logger.exception("LLM API error")
        raise RuntimeError("LLM request failed") from e
    except Exception as e:
        logger.exception("LLM request failed")
        raise RuntimeError("LLM request failed") from e

    # Normalize response text. SDKs may expose `.text` or structured output.
    text = getattr(response, "text", None)
    if not text:
        try:
            # fallback: some SDKs place content in `response.output` or similar
            text = str(response)
        except Exception:
            text = None

    if not text:
        logger.error("LLM returned empty response object: %s", repr(response))
        raise RuntimeError("LLM returned empty response")

    return text.strip()