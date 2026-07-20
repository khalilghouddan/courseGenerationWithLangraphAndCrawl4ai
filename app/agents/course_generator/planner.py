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
from app.agents.course_generator.query_builder import resolve_subject


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

    #resolve [SUBJECT] placeholder using the real subject from metadata
    subject = state.metadata.get("primary_subcategory_title") or state.metadata.get("title", "the subject")
    chapter_title = resolve_subject(chapter.get("title", ""), subject)
    lesson_title = resolve_subject(lesson.get("title", ""), subject)
    chapter_summary = resolve_subject(chapter.get("summary", ""), subject)
    lesson_goal = resolve_subject(
        lesson.get("content_markdown", lesson.get("title", "")),
        subject,
    )

    log_info(
        "PLANNER",
        "#FF5722",
        f"Planning Chapter {state.current_chapter + 1}/{total_chapters} | Lesson {state.current_lesson + 1} | '{lesson_title}'",
    )
    state.current_lesson_plan = {
        "chapter_index": state.current_chapter,
        "lesson_index": state.current_lesson,
        "chapter_title": chapter_title,
        "chapter_summary": chapter_summary,
        "title": lesson_title,
        "goal": lesson_goal,
    }

    state.current_research = []
    state.research_attempts = 0
    state.research_complete = False
    state.lesson_requires_mermaid = False
    state.template = template

    log_info("PLANNER", "#FF5722", f"Total course scope: {total_chapters} chapters | {total_lessons} lessons")

    return state