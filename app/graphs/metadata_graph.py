### Build the Metadata subgraph.

#Responsibilities:
#- Build a subgraph for the metadata generation workflow.


#StateGraph: is used to create workflows / Start mare biging and end marks end of the work flow
from langgraph.graph import StateGraph, START, END

from app.models.state import CourseState
from app.agents.metadata.agent import build_metadata_agent
from app.agents.metadata.parser import parse_metadata


def build_metadata_graph():

    workflow = StateGraph(CourseState)

    # Nodes
    workflow.add_node("metadata_agent", build_metadata_agent)
    workflow.add_node("parse_metadata", parse_metadata)

    # Edges
    workflow.add_edge(START, "metadata_agent")
    workflow.add_edge("metadata_agent", "parse_metadata")
    workflow.add_edge("parse_metadata", END)

    return workflow.compile()