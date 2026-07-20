### Course Writer Agent

#Responsibilities:
#- Generate the Markdown content for the current lesson.
#- Use only the research collected by the Researcher.
#- Decide whether a Mermaid diagram would improve the lesson.

import json

from app.models.state import CourseState
from app.services.llm import get_llm
from app.utils.logger import log_message, log_info
from app.utils.helpers import strip_markdown_fences


def _parse_writer_response(raw: str) -> dict:
    """
    Parse the LLM response for a lesson.

    The model is asked to return a JSON block with three keys:
        markdown, needs_mermaid, mermaid_description

    If JSON parsing fails, the entire response is treated as the
    markdown content with safe defaults for the other fields.
    """
    cleaned = strip_markdown_fences(raw).strip()
    try:
        data = json.loads(cleaned)
        return {
            "markdown": data.get("markdown", raw),
            "needs_mermaid": bool(data.get("needs_mermaid", False)),
            "mermaid_description": data.get("mermaid_description", ""),
        }
    except (json.JSONDecodeError, ValueError):
        #if JSON parsing fails, treat the whole response as markdown
        return {
            "markdown": raw.strip(),
            "needs_mermaid": False,
            "mermaid_description": "",
        }


def writer_node(state: CourseState) -> CourseState:

    lesson = state.current_lesson_plan
    research = state.current_research
    metadata = state.metadata

    title = lesson["title"]
    chapter = state.current_chapter
    lesson_idx = state.current_lesson
    language = metadata.get("language", "English")

    system_prompt = f"""You are an expert course author. Write a complete lesson in Markdown.

The lesson must be written entirely in {language}.
- Technically correct
- Beginner friendly when appropriate
- Well structured with clear sections
- Practical with examples
- Use code blocks when needed
- Use tables when useful
- Never invent facts — only use the provided research

Lesson Title: {title}
Lesson Goal: {lesson["goal"]}
Course Title: {metadata["title"]}
Category: {metadata.get("primary_category_title", "")}
Language: {language}

Research:
{research}

---

Return a JSON object with exactly these three keys and nothing else outside the JSON:

{{
  "markdown": "<full lesson content in Markdown, written in {language}>",
  "needs_mermaid": <true or false — true only if a diagram would significantly help understanding>,
  "mermaid_description": "<short description of the diagram to generate, or empty string>"
}}

Output ONLY the JSON object. No text before or after it."""

    with log_message("WRITER", "#8BC34A", f"Generating lesson | Chapter {chapter} Lesson {lesson_idx} | '{title}'"):
        response = get_llm().invoke(system_prompt)

    parsed = _parse_writer_response(response.content)

    word_count = len(parsed["markdown"].split())
    log_info("WRITER", "#8BC34A", f"Lesson written | {word_count} words | needs_mermaid={parsed['needs_mermaid']}")

    lesson["content_markdown"] = parsed["markdown"]
    state.lesson_requires_mermaid = parsed["needs_mermaid"]
    state.mermaid_description = parsed["mermaid_description"]
    state.current_lesson_plan = lesson

    return state