### Course Planner Agent

# Responsibilities:
# - Read the selected course template.
# - Determine the next lesson to generate.
# - Build a structured lesson plan for downstream agents.
# - Advance through chapters and lessons.


from copy import deepcopy

from app.models.state import CourseState


def _initialize_indexes(state: CourseState) -> None:
    """Initialize planner indexes the first time the graph runs."""

    if getattr(state, "current_chapter", None) is None:
        state.current_chapter = 0

    if getattr(state, "current_lesson", None) is None:
        state.current_lesson = 0


def _current_lesson(state: CourseState):
    """Return the current lesson from the template."""

    template = state.template

    chapter = template["chapters"][state.current_chapter]

    lesson = chapter["lessons"][state.current_lesson]

    return chapter, lesson


def planner_node(state: CourseState) -> CourseState:
    """
    Planner Node

    Reads the template selected by the Template Agent and prepares
    the current lesson for the Research Agent.
    """

    _initialize_indexes(state)

    template = deepcopy(state.template)

    chapter, lesson = _current_lesson(state)

    state.current_lesson_plan = {
        "chapter_index": state.current_chapter,
        "lesson_index": state.current_lesson,
        "chapter_title": chapter.get("title", ""),
        "chapter_summary": chapter.get("summary", ""),
        "title": lesson.get("title", ""),
        "goal": lesson.get("content_markdown", lesson.get("title", "")),
    }

    state.current_research = []

    state.research_attempts = 0

    state.research_complete = False

    state.lesson_requires_mermaid = False

    state.template = template

    return state