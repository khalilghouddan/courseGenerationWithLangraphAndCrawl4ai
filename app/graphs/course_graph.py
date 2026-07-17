from langgraph.graph import END, START, StateGraph

from app.agents.course_generator.formatter import formatter_node
from app.agents.course_generator.planner import planner_node
from app.agents.course_generator.researcher import researcher_node
from app.agents.course_generator.writer import writer_node
from app.models.state import CourseState


def should_continue_research(state: CourseState) -> str:
    return "writer" if state.research_complete else "research"


def needs_mermaid(state: CourseState) -> str:
    return "mermaid" if state.lesson_requires_mermaid else "formatter"


def has_more_lessons(state: CourseState) -> str:
    return "planner" if state.has_next_lesson else END


def build_course_graph():
    graph = StateGraph(CourseState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("formatter", formatter_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_conditional_edges(
        "researcher",
        should_continue_research,
        {"research": "researcher", "writer": "writer"},
    )
    graph.add_conditional_edges(
        "writer",
        needs_mermaid,
        {"mermaid": "formatter", "formatter": "formatter"},
    )
    graph.add_conditional_edges(
        "formatter",
        has_more_lessons,
        {"planner": "planner", END: END},
    )

    return graph.compile()