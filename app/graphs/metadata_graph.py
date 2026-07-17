from langgraph.graph import END, START, StateGraph

from app.agents.metadata.agent import build_metadata_agent
from app.agents.metadata.parser import parse_metadata
from app.models.state import CourseState


def build_metadata_graph():
    workflow = StateGraph(CourseState)

    workflow.add_node("metadata_agent", build_metadata_agent())
    workflow.add_node("parse_metadata", parse_metadata)

    workflow.add_edge(START, "metadata_agent")
    workflow.add_edge("metadata_agent", "parse_metadata")
    workflow.add_edge("parse_metadata", END)

    return workflow.compile()


metadata_graph = build_metadata_graph()