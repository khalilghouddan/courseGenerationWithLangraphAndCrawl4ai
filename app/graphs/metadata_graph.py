### Build the Metadata subgraph ###

#Responsibilities:
#- Build a subgraph for the metadata generation workflow.


#StateGraph: is used to create workflows / Start mare biging and end marks end of the work flow
from langgraph.graph import StateGraph, START, END
#backpack evry node can read from it and write into it
from app.models.state import CourseState
#build metadata agent
from app.agents.metadata.agent import build_metadata_agent
#parse metadata
from app.agents.metadata.parser import parse_metadata


def build_metadata_graph():

    #create an empty graph
    #graph will use same bagpack for evy node 
    workflow = StateGraph(CourseState)

    # ading nodes
    workflow.add_node("metadata_agent", build_metadata_agent)
    workflow.add_node("parse_metadata", parse_metadata)

    # start the graph
    workflow.add_edge(START, "metadata_agent")
    workflow.add_edge("metadata_agent", "parse_metadata")
    # end of it
    workflow.add_edge("parse_metadata", END)

    return workflow.compile()