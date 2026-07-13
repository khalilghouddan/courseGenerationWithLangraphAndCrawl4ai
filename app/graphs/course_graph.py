###Course Generation Graph

#Responsabilities:
#- Build the course generation workflow last graph

from langgraph.graph import START, END, StateGraph

from app.models.state import CourseState

from app.agents.course_generator.planner import planner_node
from app.agents.course_generator.researcher import researcher_node
from app.agents.course_generator.writer import writer_node
from app.agents.course_generator.formatter import formatter_node


def build_course_graph():

    workflow = StateGraph(CourseState)

    # Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("formatter", formatter_node)

    # Flow
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "formatter")
    workflow.add_edge("formatter", END)

    return workflow.compile()


course_graph = build_course_graph()