from langgraph.graph import END, START, StateGraph

from app.graphs.course_graph import build_course_graph as build_course_subgraph
from app.graphs.metadata_graph import build_metadata_graph
from app.graphs.template_graph import build_template_graph
from app.models.state import CourseState


def build_main_graph():
    workflow = StateGraph(CourseState)

    metadata_graph = build_metadata_graph()
    template_graph = build_template_graph()
    course_graph = build_course_subgraph()

    workflow.add_node("metadata", metadata_graph)
    workflow.add_node("template", template_graph)
    workflow.add_node("course", course_graph)

    workflow.add_edge(START, "metadata")
    workflow.add_edge("metadata", "template")
    workflow.add_edge("template", "course")
    workflow.add_edge("course", END)

    return workflow.compile()


def build_course_graph():
    return build_main_graph()


main_graph = build_main_graph()