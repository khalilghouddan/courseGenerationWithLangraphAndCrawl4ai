


# app/graphs/metadata_graph.py

from langgraph.graph import StateGraph, START, END

from app.models.state import CourseState
from app.agents.metadata.agent import metadata_agent
from app.agents.metadata.parser import parse_metadata


def build_metadata_graph():
    """
    Build the Metadata subgraph.

    Responsibilities:
        1. Analyze the user's prompt.
        2. Generate structured course metadata.
        3. Parse and validate the metadata.
        4. Return the updated graph state.
    """

    workflow = StateGraph(CourseState)

    # Nodes
    workflow.add_node("metadata_agent", metadata_agent)
    workflow.add_node("parse_metadata", parse_metadata)

    # Edges
    workflow.add_edge(START, "metadata_agent")
    workflow.add_edge("metadata_agent", "parse_metadata")
    workflow.add_edge("parse_metadata", END)

    return workflow.compile()