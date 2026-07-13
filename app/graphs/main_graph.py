### Main LangGraph workflow.

#Responsibilities:
#- Build the complete course generation workflow.
#TODO: think of way to make it better 


#langraph graph calling StateGraph : 
from langgraph.graph import StateGraph, START, END
from app.models.state import CourseState
#small graphes from the other files
from app.graphs.metadata_graph import build_metadata_graph
from app.graphs.template_graph import build_template_graph
from app.graphs.course_graph import build_course_graph


def build_main_graph():
   

    workflow = StateGraph(CourseState)

    # Subgraphs
    metadata_graph = build_metadata_graph()
    template_graph = build_template_graph()
    course_graph = build_course_graph()

    # Register nodes
    workflow.add_node("metadata", metadata_graph)
    workflow.add_node("template", template_graph)
    workflow.add_node("course", course_graph)

    # Workflow
    workflow.add_edge(START, "metadata")
    workflow.add_edge("metadata", "template")
    workflow.add_edge("template", "course")
    workflow.add_edge("course", END)

    return workflow.compile()

main_graph = build_main_graph()