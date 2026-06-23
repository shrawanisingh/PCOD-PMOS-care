from agents.supervisor import run_supervisor
from agents.clinical import run_clinical
from agents.metabolic import run_metabolic
from agents.lifestyle import run_lifestyle
from agents.planner import run_planner

from rag.query_rewriter import rewrite_query
from rag.retriever import retrieve
from rag.context_builder import build_context


# -----------------------------
# Query Rewriter Node
# -----------------------------
def rewrite_node(state):

    query = state["query"]

    rewritten_query = rewrite_query(
        query
    )

    return {
        "rewritten_query": rewritten_query
    }


# -----------------------------
# Retrieval Node
# -----------------------------
def retrieval_node(state):

    query = state["rewritten_query"]

    docs = retrieve(
        query,
        k=5
    )

    return {
        "retrieved_docs": docs
    }


# -----------------------------
# Context Builder Node
# -----------------------------
def context_node(state):

    context = build_context(
        state["retrieved_docs"]
    )

    return {
        "context": context
    }


# -----------------------------
# Supervisor Node
# -----------------------------
def supervisor_node(state):

    routing = run_supervisor(
        state["query"]
    )

    return {
        "routing": routing
    }


# -----------------------------
# Clinical Agent
# -----------------------------
def clinical_node(state):

    prompt = f"""
Medical Evidence:

{state["context"]}

Patient Information:

{state["query"]}

Act as a gynecologist specializing in PCOS.

Provide:
1. Key observations
2. Clinical concerns
3. Suggested investigations

Limit response to 150 words.
"""

    result = run_clinical(
        prompt
    )

    return {
        "clinical": [result]
    }


# -----------------------------
# Metabolic Agent
# -----------------------------
def metabolic_node(state):

    prompt = f"""
Medical Evidence:

{state["context"]}

Patient Information:

{state["query"]}

Act as an endocrinologist.

Provide:
1. Metabolic concerns
2. Insulin resistance risks
3. Hormonal observations

Limit response to 150 words.
"""

    result = run_metabolic(
        prompt
    )

    return {
        "metabolic": [result]
    }


# -----------------------------
# Lifestyle Agent
# -----------------------------
def lifestyle_node(state):

    prompt = f"""
Medical Evidence:

{state["context"]}

Patient Information:

{state["query"]}

Act as a lifestyle and PCOS wellness coach.

Provide:
1. Sleep recommendations
2. Stress management
3. Diet suggestions
4. Exercise suggestions

Limit response to 150 words.
"""

    result = run_lifestyle(
        prompt
    )

    return {
        "lifestyle": [result]
    }


# -----------------------------
# Aggregator Node
# -----------------------------
def aggregator_node(state):

    clinical = "\n".join(
        state.get("clinical", [])
    )

    metabolic = "\n".join(
        state.get("metabolic", [])
    )

    lifestyle = "\n".join(
        state.get("lifestyle", [])
    )

    combined = f"""
CLINICAL SPECIALIST:
{clinical}

--------------------------------

METABOLIC SPECIALIST:
{metabolic}

--------------------------------

LIFESTYLE SPECIALIST:
{lifestyle}
"""

    return {
        "combined": combined
    }


# -----------------------------
# Planner Node
# -----------------------------
def planner_node(state):

    prompt = f"""
You are the final PCOS care coordinator.

Patient:

{state["query"]}

Specialist Opinions:

{state["combined"]}

Create a final report with:

1. Key Observations
2. Possible Contributing Factors
3. Lifestyle Suggestions
4. Questions for Healthcare Provider
5. When to Seek Medical Attention

Keep the report evidence-based and concise.
"""

    report = run_planner(
        prompt
    )

    return {
        "final_report": report
    }