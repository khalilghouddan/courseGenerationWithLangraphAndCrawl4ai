### Course Planner Agent

#Responsibilities:
#- Read the selected course template.
#- Determine the next lesson to generate.
#- Build a structured lesson plan for downstream agents.
#- Advance through chapters and lessons.

from app.utils.logger import log_info
from copy import deepcopy

from app.models.state import CourseState
from app.utils.logger import log_message


def _initialize_indexes(state: CourseState) -> None:
    if getattr(state, "current_chapter", None) is None:
        state.current_chapter = 0
    if getattr(state, "current_lesson", None) is None:
        state.current_lesson = 0


def _current_lesson(state: CourseState):
    template = state.template
    chapter = template["chapters"][state.current_chapter]
    lesson = chapter["lessons"][state.current_lesson]
    return chapter, lesson


def planner_node(state: CourseState) -> CourseState:

    _initialize_indexes(state)

    template = deepcopy(state.template)

    total_chapters = len(template["chapters"])
    total_lessons = sum(len(ch["lessons"]) for ch in template["chapters"])

    chapter, lesson = _current_lesson(state)

    chapter_title = chapter.get("title", "")
    lesson_title = lesson.get("title", "")

    log_info(
        "PLANNER",
        "#FF5722",
        f"Planning Chapter {state.current_chapter + 1}/{total_chapters} | Lesson {state.current_lesson + 1} ",
    )
    state.current_lesson_plan = {
        "chapter_index": state.current_chapter,
        "lesson_index": state.current_lesson,
        "chapter_title": chapter_title,
        "chapter_summary": chapter.get("summary", ""),
        "title": lesson_title,
        "goal": lesson.get("content_markdown", lesson.get("title", "")),
    }

    state.current_research = []
    state.research_attempts = 0
    state.research_complete = False
    state.lesson_requires_mermaid = False
    state.template = template

    log_info("PLANNER", "#FF5722", f"Total course scope: {total_chapters} chapters | {total_lessons} lessons")

    return state