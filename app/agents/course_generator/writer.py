from app.models.state import CourseState


def writer_node(state: CourseState) -> CourseState:
    state.lesson_requires_mermaid = False
    return state
