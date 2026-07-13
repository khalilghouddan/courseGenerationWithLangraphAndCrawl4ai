"""
Template Agent LangGraph.

This graph is responsible for selecting the most appropriate course
template based on the metadata produced by the Metadata Agent.
"""

from langgraph.graph import START, END, StateGraph

from app.models.state import CourseState
from app.agents.template.agent import TemplateAgent


def validate_metadata(state: CourseState) -> CourseState:

    if state.metadata is None:
        raise ValueError("Metadata is required before template selection.")

    return state


def select_template(state: CourseState) -> CourseState:

    return TemplateAgent.invoke(state)


def validate_template(state: CourseState) -> CourseState:

    if state.template is None:
        raise ValueError("Template selection failed.")

    return state


def build_template_graph():
    """
    Build the Template Selection subgraph.
    """

    builder = StateGraph(CourseState)

    # Register nodes
    builder.add_node("validate_metadata", validate_metadata)
    builder.add_node("select_template", select_template)
    builder.add_node("validate_template", validate_template)

    # Define workflow
    builder.add_edge(START, "validate_metadata")
    builder.add_edge("validate_metadata", "select_template")
    builder.add_edge("select_template", "validate_template")
    builder.add_edge("validate_template", END)

    return builder.compile()


template_graph = build_template_graph()