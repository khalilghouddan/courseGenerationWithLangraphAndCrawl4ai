### Course Writer Agent

#Responsibilities:
#- Generate the Markdown content for the current lesson.
#- Use only the research collected by the Researcher.
#- Decide whether a Mermaid diagram would improve the lesson.


from pydantic import BaseModel, Field
from langchain_core.runnables import Runnable

from app.models.state import CourseState
from app.services.llm import get_llm
from app.utils.logger import log_message


#structured output schema – Pydantic ensures reliable tool-calling
class LessonOutput(BaseModel):
    markdown: str = Field(description="The full lesson content written in Markdown.")
    needs_mermaid: bool = Field(description="True if a Mermaid diagram would improve understanding of this lesson.")
    mermaid_description: str = Field(description="A description of the Mermaid diagram to generate. Empty string if needs_mermaid is false.")


def build_writer_agent() -> Runnable:

    def writer_node(state: CourseState) -> CourseState:
        lesson = state.current_lesson_plan
        research = state.current_research
        metadata = state.metadata

        title = lesson["title"]
        chapter = state.current_chapter
        lesson_idx = state.current_lesson

        system_prompt = f"""
You are an expert course author.

Write a complete lesson in Markdown.

The lesson must be:

- Technically correct
- Beginner friendly when appropriate
- Well structured
- Practical
- Easy to understand
- Use examples
- Use code blocks when needed
- Use tables when useful
- Never invent facts
- Only use the provided research.

Lesson Title:
{title}

Lesson Goal:
{lesson["goal"]}

Course Title:
{metadata["title"]}

Category:
{metadata.get("primary_category_title", "")}

Research:

{research}
"""

        with log_message("WRITER", "#8BC34A", f"Generating lesson | Chapter {chapter} Lesson {lesson_idx} | '{title}'"):
            response = get_llm().with_structured_output(LessonOutput).invoke(system_prompt)

        word_count = len(response.markdown.split())
        with log_message("WRITER", "#8BC34A", f"Lesson written | {word_count} words | needs_mermaid={response.needs_mermaid}"):
            lesson["content_markdown"] = response.markdown
            state.lesson_requires_mermaid = response.needs_mermaid
            state.mermaid_description = response.mermaid_description
            state.current_lesson_plan = lesson

        return state

    return writer_node


writer_node = build_writer_agent()