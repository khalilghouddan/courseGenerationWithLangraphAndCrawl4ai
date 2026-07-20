### Course Writer Agent

# Responsibilities:
# - Generate the Markdown content for the current lesson.
# - Use only the research collected by the Researcher.
# - Decide whether a Mermaid diagram would improve the lesson.



from langchain_core.runnables import Runnable

from app.models.state import CourseState
from app.services.llm import get_llm


def build_writer_agent() -> Runnable:
    """
    Build the Writer agent.
    """

    def writer_node(state: CourseState) -> CourseState:
        lesson = state.current_lesson_plan

        research = state.current_research

        metadata = state.metadata

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
{lesson["title"]}

Lesson Goal:
{lesson["goal"]}

Course Title:
{metadata["title"]}

Difficulty:
{metadata["difficulty"]}

Research:

{research}
"""

        response = get_llm().with_structured_output(
            {
                "name": "LessonOutput",
                "schema": {
                    "type": "object",
                    "properties": {
                        "markdown": {
                            "type": "string"
                        },
                        "needs_mermaid": {
                            "type": "boolean"
                        },
                        "mermaid_description": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "markdown",
                        "needs_mermaid",
                        "mermaid_description"
                    ]
                }
            }
        ).invoke(system_prompt)

        lesson["content_markdown"] = response["markdown"]

        state.lesson_requires_mermaid = response["needs_mermaid"]

        state.mermaid_description = response["mermaid_description"]

        state.current_lesson_plan = lesson

        return state

    return writer_node


writer_node = build_writer_agent()