from langchain_core.runnables import Runnable

from app.agents.metadata.models import CourseMetadata
from app.models.state import CourseState


def build_metadata_agent() -> Runnable:
    def metadata_agent(state: CourseState) -> CourseState:
        prompt = state.prompt.strip() if state.prompt else ""
        topic = prompt or "general learning"
        metadata = CourseMetadata(
            title=f"{topic.title()} Course",
            headline=f"Learn {topic.lower()} with a practical, step-by-step approach",
            description=(
                f"This course introduces {topic.lower()} in a concise, beginner-friendly way. "
                "It focuses on clarity, examples, and practical understanding."
            ),
            objectives=["Understand the topic", "Apply the basics", "Build confidence"],
            prerequisites=["Basic curiosity"],
            target_audiences="Beginners and self-directed learners",
            primary_category_title="Education",
            primary_subcategory_title="Learning",
            duration="2 hours",
            language="English",
        )
        state.metadata = metadata.model_dump()
        return state

    return metadata_agent