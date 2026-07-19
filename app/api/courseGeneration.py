"""
Course Generation Graph

Responsibilities:
- Build the workflow for generating the course content.
- Orchestrate the planner, researcher, writer, formatter, and Mermaid generation.
- Allow the researcher to retry until sufficient information is collected.
"""

from langgraph.graph import StateGraph, START, END

from app.models.state import CourseState

from app.agents.course_generator.planner import planner_node
from app.agents.course_generator.researcher import researcher_node
from app.agents.course_generator.writer import writer_node
from app.agents.course_generator.formatter import formatter_node


def should_continue_research(state: CourseState) -> str:
    """
    Decide whether the current lesson needs additional research.

    Returns:
        "research" -> Search and scrape more sources.
        "writer"   -> Enough information collected.
    """
    if state.research_complete:
        return "writer"

    return "research"


def needs_mermaid(state: CourseState) -> str:
    """
    Decide whether the generated lesson should include a Mermaid diagram.

    Returns:
        "formatter" -> No Mermaid diagram required.
        "mermaid"   -> Generate a Mermaid diagram before formatting.
    """
    if state.lesson_requires_mermaid:
        return "mermaid"

    return "formatter"


def has_more_lessons(state: CourseState) -> str:
    """
    Determine whether there are more lessons remaining.

    Returns:
        "planner" -> Continue with the next lesson.
        END       -> Course generation completed.
    """
    if state.has_next_lesson:
        return "planner"

    return END


def build_course_graph():
    """
    Build the Course Generation subgraph.

    Workflow:

        Planner
            ↓
        Research
            │
            ├── Not enough information ─────┐
            │                               │
            └──────────────► Research ◄─────┘
            │
            ▼
        Writer
            │
            ├── Mermaid needed?
            │
            ├── Yes ─► Mermaid Generator
            │             │
            └──── No ─────┘
                    │
                    ▼
                Formatter
                    │
                    ├── Next lesson? ──► Planner
                    │
                    └── No ───────────► END
    """

    graph = StateGraph(CourseState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)

    # TODO
    # graph.add_node("mermaid", mermaid_node)

    graph.add_node("formatter", formatter_node)

    graph.add_edge(START, "planner")

    graph.add_edge("planner", "researcher")

    graph.add_conditional_edges(
        "researcher",
        should_continue_research,
        {
            "research": "researcher",
            "writer": "writer",
        },
    )

    graph.add_conditional_edges(
        "writer",
        needs_mermaid,
        {
            "mermaid": "formatter",  # Replace with "mermaid" when implemented
            "formatter": "formatter",
        },
    )

    # graph.add_edge("mermaid", "formatter")

    graph.add_conditional_edges(
        "formatter",
        has_more_lessons,
        {
            "planner": "planner",
            END: END,
        },
    )

    return graph.compile()