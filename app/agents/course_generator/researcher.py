from app.models.state import CourseState


def researcher_node(state: CourseState) -> CourseState:
    state.research_complete = True
    return state
