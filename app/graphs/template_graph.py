### TEMPLATE GRAPH #

# Responsible:
#- orchestrating the template workflow

#TODO: verify if it is the good template
#TODO: fuction corrction and gggg



#langgraph.graph END: end of the main graph / START: start of the main graph / STateGraph: the main graph structure
from langgraph.graph import END, START, StateGraph
#template agent node
from app.agents.template.agent import select_template as select_template_node
#memory state
from app.models.state import CourseState
from app.utils.logger import log_message


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

    def run_select_template(state: CourseState) -> CourseState:
        with log_message("TEMPLATE_GRAPH", "#FF9800", "Selecting template"):
            return select_template(state)

    def run_validate_template(state: CourseState) -> CourseState:
        with log_message("TEMPLATE_GRAPH", "#FF9800", "Validating template"):
            return validate_template(state)

    builder.add_node("select_template", run_select_template)
    builder.add_node("validate_template", run_validate_template)

    builder.add_edge(START, "select_template")
    builder.add_edge("select_template", "validate_template")
    builder.add_edge("validate_template", END)
    
    return builder.compile()


template_graph = build_template_graph()