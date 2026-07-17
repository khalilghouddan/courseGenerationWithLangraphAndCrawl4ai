from langgraph.graph import END, START, StateGraph

from app.agents.template.agent import select_template as select_template_node
from app.models.state import CourseState


def validate_metadata(state: CourseState) -> CourseState:
    if not state.metadata:
        raise ValueError("Metadata is required before template selection.")
    return state


def select_template(state: CourseState) -> CourseState:
    return select_template_node(state)


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

    return builder.compile()


template_graph = build_template_graph()