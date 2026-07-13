"""
Template Agent LangGraph.

This graph is responsible for selecting the most appropriate course
template based on the metadata produced by the Metadata Agent.
"""

from langgraph.graph import START, END, StateGraph

from app.models.state import CourseState
from app.agents.template.agent import TemplateAgent


template_agent = TemplateAgent()


def validate_metadata(state: CourseState) -> CourseState:
    """
    Ensure metadata exists before selecting a template.
    """
    if state.metadata is None:
        raise ValueError("Metadata is required before template selection.")

    return state


def select_template(state: CourseState) -> CourseState:
    """
    Execute the Template Agent.
    """
    return template_agent.invoke(state)


def validate_template(state: CourseState) -> CourseState:
    """
    Ensure a template has been selected.
    """
    if state.template is None:
        raise ValueError("Template selection failed.")

    return state


builder = StateGraph(CourseState)

builder.add_node("validate_metadata", validate_metadata)
builder.add_node("select_template", select_template)
builder.add_node("validate_template", validate_template)

builder.add_edge(START, "validate_metadata")
builder.add_edge("validate_metadata", "select_template")
builder.add_edge("select_template", "validate_template")
builder.add_edge("validate_template", END)

template_graph = builder.compile()