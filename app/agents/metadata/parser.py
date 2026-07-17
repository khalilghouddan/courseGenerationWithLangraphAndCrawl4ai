from app.agents.metadata.models import CourseMetadata
from app.models.state import CourseState


def parse_metadata(state: CourseState) -> CourseState:
    try:
        metadata_payload = state.metadata or {}
        parsed = CourseMetadata.model_validate(metadata_payload)
        state.metadata = parsed.model_dump()
        return state
    except Exception as exc:
        raise ValueError(f"Invalid metadata: {exc}") from exc