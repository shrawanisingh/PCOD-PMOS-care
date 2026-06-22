import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Allow running in a mocked mode for development/testing when the API key is missing
_MOCK = os.getenv("MOCK_LLM", "0") == "1"
_API_KEY = os.getenv("GEMINI_API_KEY")
if not _API_KEY and not _MOCK:
    raise ValueError("GEMINI_API_KEY not set. Please add it to your environment or .env file, or enable MOCK_LLM=1 for local testing.")

if _API_KEY:
    client = genai.Client(api_key=_API_KEY)
else:
    client = None

MODEL = "gemini-2.5-flash"


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
    if _MOCK:
        logger.info("MOCK_LLM enabled — returning canned response")
        return f"[MOCK] This is a mocked LLM response for input: {user_prompt}"

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=300
            )
        )
    except genai.errors.ClientError as e:
        # Handle API quota/rate-limit errors with a safe fallback for local testing.
        msg = str(e)
        if getattr(e, "status_code", None) == 429 or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower():
            logger.warning("LLM quota or rate limit hit: %s", msg)
            return (
                "[LLM unavailable: quota exceeded. Returning placeholder response for testing. "
                "Replace GEMINI_API_KEY, upgrade quota, or retry later.]"
            )
        logger.exception("LLM client error")
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