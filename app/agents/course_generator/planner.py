from app.models.state import CourseState


def planner_node(state: CourseState) -> CourseState:
    state.research_complete = False
    state.has_next_lesson = True
    state.lesson_requires_mermaid = False
    return state
