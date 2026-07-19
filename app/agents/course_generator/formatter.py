"""
Course Formatter Node

Responsibilities:
- Insert the generated lesson into the course template.
- Update course metadata.
- Advance the lesson cursor.
"""

from copy import deepcopy

from app.models.state import CourseState


def formatter_node(state: CourseState) -> CourseState:
    """
    Format the generated lesson into the course template.

    Expected state:

    state.template
        The selected course template loaded from the database.

    state.current_chapter
        Current chapter index.

    state.current_lesson
        Current lesson index.

    state.current_lesson_plan
        {
            "title": "...",
            "content_markdown": "..."
        }
    """

    template = deepcopy(state.template)

    chapter_index = state.current_chapter
    lesson_index = state.current_lesson

    lesson = template["chapters"][chapter_index]["lessons"][lesson_index]

    generated_lesson = getattr(state, "current_lesson_plan", {})
    lesson["title"] = generated_lesson.get("title", lesson.get("title", ""))
    lesson["content_markdown"] = generated_lesson.get("content_markdown", "")

    state.template = template

    _update_metadata(state)

    _move_to_next_lesson(state)

    return state


def _move_to_next_lesson(state: CourseState) -> None:
    """
    Move the course cursor to the next lesson.
    """

    chapters = state.template["chapters"]

    chapter_index = state.current_chapter
    lesson_index = state.current_lesson + 1

    if lesson_index < len(chapters[chapter_index]["lessons"]):
        state.current_lesson = lesson_index
        state.has_next_lesson = True
        return

    chapter_index += 1

    if chapter_index < len(chapters):
        state.current_chapter = chapter_index
        state.current_lesson = 0
        state.has_next_lesson = True
        return

    state.has_next_lesson = False


def _update_metadata(state: CourseState) -> None:
    """
    Update template metadata.
    """

    metadata = state.template["metadata"]

    metadata["has_content"] = True

    lesson_count = 0
    estimated_minutes = 0

    for chapter in state.template["chapters"]:
        for lesson in chapter["lessons"]:

            if lesson["content_markdown"]:
                lesson_count += 1

                # Rough estimate:
                # ~250 words/min reading speed
                words = len(lesson["content_markdown"].split())
                estimated_minutes += max(5, words // 250)

    metadata["lesson_count"] = lesson_count
    metadata["chapter_count"] = len(state.template["chapters"])
    metadata["estimated_study_time_minutes"] = estimated_minutes