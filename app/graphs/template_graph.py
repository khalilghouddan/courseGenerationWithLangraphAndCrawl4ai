### TEMPLATE GRAPH #

# Responsible:
#- orchestrating the template workflow

#TODO: verify if it is the good template


#langgraph.graph END: end of the main graph / START: start of the main graph / STateGraph: the main graph structure
from langgraph.graph import END, START, StateGraph
#template agent node
from app.agents.template.agent import select_template as select_template_node
#memory state
from app.models.state import CourseState
from app.utils.logger import log_message


#verify if we have the metadata before selecting the template
def validate_metadata(state: CourseState) -> CourseState:
    if not state.metadata:
        raise ValueError("Metadata is required before template selection.")
    return state

#select the template
def select_template(state: CourseState) -> CourseState:
    return select_template_node(state)

#validate the template exestance 
def validate_template(state: CourseState) -> CourseState:
    if not state.template:
        raise ValueError("Template selection failed.")
    return state


def build_template_graph():

    builder = StateGraph(CourseState)

    builder.add_node("validate_metadata", validate_metadata)
    builder.add_node("select_template", select_template)
    builder.add_node("validate_template", validate_template)

    builder.add_edge(START, "validate_metadata")
    builder.add_edge("validate_metadata", "select_template")
    builder.add_edge("select_template", "validate_template")
    builder.add_edge("validate_template", END)
    
    with log_message("TEMPLATE_GRAPH", "#FF9800", "Building template workflow"):
        return builder.compile()


template_graph = build_template_graph()