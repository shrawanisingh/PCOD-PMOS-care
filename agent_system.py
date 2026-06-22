# agent_system.py
import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import prompts

# Fetch the built-in Codespace token automatically
token = os.environ.get("GITHUB_TOKEN")

if not token:
    raise ValueError("GITHUB_TOKEN not found. Make sure you are inside GitHub Codespaces.")

# Initialize the GitHub Models client
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(token)
)

# Using GPT-4o for robust agentic execution
MODEL_NAME = "gpt-4o"

def ask_github_model(system_prompt: str, user_content: str, expect_json: bool = False) -> str:
    """Helper function to cleanly call the GitHub Model API layer."""
    kwargs = {
        "messages": [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_content)
        ],
        "model": MODEL_NAME
    }
    
    # Enable strict JSON response formatting if required
    if expect_json:
        kwargs["response_format"] = {"type": "json_object"}
        
    response = client.complete(**kwargs)
    return response.choices[0].message.content

def run_pcos_care_system(user_query: str):
    print(f"🚀 Initializing care plan orchestration for: '{user_query}'\n")
    
    # ==========================================
    # STEP 1: Supervisor / Router Phase
    # ==========================================
    print("➔ Supervisor is assessing routing criteria...")
    router_instruction = f"{prompts.SUPERVISOR_PROMPT}\nReturn your output strictly as a JSON object matching this structure:\n{{\"selected_agents\": [\"metabolic\", \"clinical\", \"lifestyle\"]}}"
    
    router_raw = ask_github_model(router_instruction, f"Patient Query: {user_query}", expect_json=True)
    
    # Parse the routing decision cleanly
    decision = json.loads(router_raw)
    selected_agents = decision.get("selected_agents", [])
    print(f"➔ Supervisor selected active tracks: {selected_agents}\n")
    
    # ==========================================
    # STEP 2: Specialist Generation Phase
    # ==========================================
    specialist_insights = {}
    
    if 'metabolic' in selected_agents:
        print("➔ Consulting Metabolic & Nutritional AI Specialist...")
        res = ask_github_model(prompts.METABOLIC_PROMPT, f"Patient Concerns: {user_query}")
        specialist_insights['Metabolic & Nutrition Report'] = res
        
    if 'clinical' in selected_agents:
        print("➔ Consulting Clinical Endocrine Specialist AI...")
        res = ask_github_model(prompts.CLINICAL_PROMPT, f"Patient Concerns: {user_query}")
        specialist_insights['Clinical Endocrine Report'] = res
        
    if 'lifestyle' in selected_agents:
        print("➔ Consulting Lifestyle & Stress Management Coach AI...")
        res = ask_github_model(prompts.LIFESTYLE_PROMPT, f"Patient Concerns: {user_query}")
        specialist_insights['Lifestyle & Stress Report'] = res

    # ==========================================
    # STEP 3: Synthesis Phase
    # ==========================================
    print("\n➔ Synthesizing specialist components into the final roadmap...")
    
    # Format the separate reports to present to the final coordinator agent
    compiled_reports = ""
    for title, content in specialist_insights.items():
        compiled_reports += f"### {title}\n{content}\n\n"
        
    final_input = f"Original Query: {user_query}\n\nSpecialist Sub-Reports:\n{compiled_reports}"
    
    final_care_plan = ask_github_model(prompts.SYNTHESIZER_PROMPT, final_input)
    return final_care_plan

if __name__ == "__main__":
    sample_query = "I am experiencing heavy sugar cravings around 4 PM, my periods are 45 days apart, and I feel completely exhausted after intense workouts."
    
    try:
        care_plan = run_pcos_care_system(sample_query)
        print("\n================ FINAL CARE ROADMAP ================\n")
        print(care_plan)
    except Exception as e:
        print(f"❌ An error occurred during agent collaboration: {e}")