### METADATA GRAPH #

#Responsible:
#- orchestrating the metadata workflow


from langgraph.graph import END, START, StateGraph
#importing the agent 
from app.agents.metadata.agent import build_metadata_agent
#parse data laggraph fuctoon
from app.agents.metadata.parser import parse_metadata
#memory state
from app.models.state import CourseState
#log fuction 
from app.utils.logger import log_message

def build_metadata_graph():

    workflow = StateGraph(CourseState)

    workflow.add_node("metadata_agent", build_metadata_agent())
    workflow.add_node("parse_metadata", parse_metadata)

    workflow.add_edge(START, "metadata_agent")
    workflow.add_edge("metadata_agent", "parse_metadata")
    workflow.add_edge("parse_metadata", END)
    
    with log_message("METADATA_GRAPH", "#00B8D9", "compile"):
        return workflow.compile()


metadata_graph = build_metadata_graph()