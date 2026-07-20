### Course Formatter Node

#Responsibilities:
#- Insert the generated lesson into the course template.
#- Update course metadata.
#- Advance the lesson cursor.

from copy import deepcopy

from app.models.state import CourseState
from app.utils.logger import log_message


def formatter_node(state: CourseState) -> CourseState:

    template = deepcopy(state.template)

    chapter_index = state.current_chapter
    lesson_index = state.current_lesson

    generated_lesson = getattr(state, "current_lesson_plan", {})
    lesson_title = generated_lesson.get("title", "")

    with log_message(
        "FORMATTER",
        "#9C27B0",
        f"Inserting lesson into template | Chapter {chapter_index} Lesson {lesson_index} | '{lesson_title}'",
    ):
        lesson = template["chapters"][chapter_index]["lessons"][lesson_index]
        lesson["title"] = generated_lesson.get("title", lesson.get("title", ""))
        lesson["content_markdown"] = generated_lesson.get("content_markdown", "")
        state.template = template

    with log_message("FORMATTER", "#9C27B0", "Updating course metadata"):
        _update_metadata(state)

    with log_message("FORMATTER", "#9C27B0", "Advancing lesson cursor"):
        _move_to_next_lesson(state)

    chapters = state.template["chapters"]
    if state.has_next_lesson:
        next_chapter = state.current_chapter
        next_lesson = state.current_lesson
        next_title = chapters[next_chapter]["lessons"][next_lesson].get("title", "")
        with log_message("FORMATTER", "#9C27B0", f"Next: Chapter {next_chapter} Lesson {next_lesson} | '{next_title}'"):
            pass
    else:
        with log_message("FORMATTER", "#9C27B0", "All lessons complete — course generation finished"):
            pass

    return state


def _move_to_next_lesson(state: CourseState) -> None:

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

    metadata = state.template.setdefault("metadata", {})
    metadata["has_content"] = True

    lesson_count = 0
    estimated_minutes = 0

    for chapter in state.template["chapters"]:
        for lesson in chapter["lessons"]:
            if lesson["content_markdown"]:
                lesson_count += 1
                words = len(lesson["content_markdown"].split())
                estimated_minutes += max(5, words // 250)

    metadata["lesson_count"] = lesson_count
    metadata["chapter_count"] = len(state.template["chapters"])
    metadata["estimated_study_time_minutes"] = estimated_minutes