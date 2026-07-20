### THE MAIN GRAPH ###

# Responsible:
#- orchestraing the work flow 
#- defining the main graph structure
#-

#TODO: verify if the one state is good here


#langgraph.graph END: end of the main graph / START: start of the main graph / STateGraph: the main graph structure
from langgraph.graph import END, START, StateGraph
#importing the subgraphs
from app.graphs.course_graph import build_course_graph 
from app.graphs.metadata_graph import build_metadata_graph
from app.graphs.template_graph import build_template_graph
# CourseState is memory state of all the nodes 
from app.models.state import CourseState
#log fuction 
from app.utils.logger import log_message

#main  in graph fucction
def build_main_graph():

    workflow = StateGraph(CourseState)

    metadata_graph = build_metadata_graph()
    template_graph = build_template_graph()
    course_graph = build_course_graph()

    # Wrap subgraph executions to log them in order during request execution
    async def run_metadata(state: CourseState):
        with log_message("MAIN_GRAPH", "#7B61FF", "Starting Metadata Phase"):
            return await metadata_graph.ainvoke(state)

    async def run_template(state: CourseState):
        with log_message("MAIN_GRAPH", "#7B61FF", "Starting Template Selection Phase"):
            return await template_graph.ainvoke(state)

    async def run_course(state: CourseState):
        with log_message("MAIN_GRAPH", "#7B61FF", "Starting Course Generation Phase"):
            return await course_graph.ainvoke(state)

    workflow.add_node("metadata", run_metadata)
    workflow.add_node("template", run_template)
    workflow.add_node("course", run_course)

    workflow.add_edge(START, "metadata")
    workflow.add_edge("metadata", "template")
    workflow.add_edge("template", "course")
    workflow.add_edge("course", END)

    return workflow.compile()

# build instance the main graph
main_graph = build_main_graph()