from langgraph.graph import StateGraph

from graph.state import PatientState

from graph.nodes import (
    rewrite_node,
    retrieval_node,
    context_node,
    supervisor_node,
    clinical_node,
    metabolic_node,
    lifestyle_node,
    aggregator_node,
    planner_node
)

# Initialize graph
workflow = StateGraph(PatientState)

# -----------------------
# RAG Nodes
# -----------------------

workflow.add_node(
    "rewrite",
    rewrite_node
)

workflow.add_node(
    "retrieval",
    retrieval_node
)

workflow.add_node(
    "context",
    context_node
)

# -----------------------
# Supervisor
# -----------------------

workflow.add_node(
    "supervisor",
    supervisor_node
)

# -----------------------
# Specialist Agents
# -----------------------

workflow.add_node(
    "clinical",
    clinical_node
)

workflow.add_node(
    "metabolic",
    metabolic_node
)

workflow.add_node(
    "lifestyle",
    lifestyle_node
)

# -----------------------
# Aggregation & Planning
# -----------------------

workflow.add_node(
    "aggregator",
    aggregator_node
)

workflow.add_node(
    "planner",
    planner_node
)

# -----------------------
# Entry Point
# -----------------------

workflow.set_entry_point(
    "rewrite"
)

# -----------------------
# Routing Logic
# -----------------------

def route(state):

    routing = state["routing"]

    nodes = []

    if routing.get("clinical"):
        nodes.append("clinical")

    if routing.get("metabolic"):
        nodes.append("metabolic")

    if routing.get("lifestyle"):
        nodes.append("lifestyle")

    return nodes

# -----------------------
# RAG Pipeline
# -----------------------

workflow.add_edge(
    "rewrite",
    "retrieval"
)

workflow.add_edge(
    "retrieval",
    "context"
)

workflow.add_edge(
    "context",
    "supervisor"
)

# -----------------------
# Dynamic Agent Routing
# -----------------------

workflow.add_conditional_edges(
    "supervisor",
    route
)

# -----------------------
# Parallel Agent Execution
# -----------------------

workflow.add_edge(
    "clinical",
    "aggregator"
)

workflow.add_edge(
    "metabolic",
    "aggregator"
)

workflow.add_edge(
    "lifestyle",
    "aggregator"
)

# -----------------------
# Final Report Generation
# -----------------------

workflow.add_edge(
    "aggregator",
    "planner"
)

# -----------------------
# Finish Point
# -----------------------

workflow.set_finish_point(
    "planner"
)

# Compile Graph
graph = workflow.compile()