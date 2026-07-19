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
    metadata_agent_fn = build_metadata_agent()

    # Wrap node executions to log them in order during request execution
    def run_metadata_agent(state: CourseState) -> CourseState:
        with log_message("METADATA_GRAPH", "#7B61F", "Running metadata agent"):
            return metadata_agent_fn(state)

    def run_parse_metadata(state: CourseState) -> CourseState:
        with log_message("METADATA_GRAPH", "#7B61F", "Parsing metadata"):
            return parse_metadata(state)

    workflow.add_node("metadata_agent", run_metadata_agent)
    workflow.add_node("parse_metadata", run_parse_metadata)

    workflow.add_edge(START, "metadata_agent")
    workflow.add_edge("metadata_agent", "parse_metadata")
    workflow.add_edge("parse_metadata", END)
    
    return workflow.compile()


metadata_graph = build_metadata_graph()