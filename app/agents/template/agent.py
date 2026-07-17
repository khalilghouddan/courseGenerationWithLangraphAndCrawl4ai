from app.models.state import CourseState


def select_template(state: CourseState) -> CourseState:
    metadata = state.metadata
    if not metadata:
        raise ValueError("Metadata must be generated before selecting a template.")

    state.template = {
        "id": "default-template",
        "title": "Default course template",
        "language": metadata.get("language", "English"),
        "description": "A simple, structured learning template",
    }
    return state