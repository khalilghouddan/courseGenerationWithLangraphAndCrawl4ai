from app.models.course import CourseOutput
from app.models.state import CourseState


def formatter_node(state: CourseState) -> CourseState:
    prompt = state.prompt.strip() or "course"
    title = f"{prompt.title()} Course"
    state.course = CourseOutput(
        title=title,
        headline=f"A structured course on {prompt.lower()}",
        description=(
            f"This course provides a practical introduction to {prompt.lower()} with a clear progression "
            "from fundamentals to applied learning."
        ),
        objectives=["Understand the topic", "Apply practical examples", "Review key concepts"],
        prerequisites=["Basic curiosity"],
        target_audiences="Beginners and self-directed learners",
        primary_category_title="Education",
        primary_subcategory_title="Training",
        duration="2 hours",
        language="English",
        urls_scraped=state.urls_scraped,
        realcoursebody={
            "title": title,
            "chapters": [
                {"title": "Introduction", "lessons": ["What you will learn", "How to get started"]},
                {"title": "Core Concepts", "lessons": ["Key ideas", "Practice exercise"]},
            ],
        },
    )
    state.realcoursebody = state.course.realcoursebody
    state.structured_response = state.course.model_dump()
    state.has_next_lesson = False
    return state
