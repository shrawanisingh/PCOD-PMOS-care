import os
import sys

# Ensure project root is on sys.path so `services` can be imported when running tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Enable mock mode before importing the service so it doesn't require a real key
os.environ.setdefault("MOCK_LLM", "1")

from services.llm_service import ask_llm


def main():
    resp = ask_llm("SYSTEM: Test mock", "User input for mock test")
    assert resp.startswith("[MOCK]"), f"Unexpected mock response: {resp}"
    print("MOCK test passed:\n", resp)


if __name__ == "__main__":
    main()
