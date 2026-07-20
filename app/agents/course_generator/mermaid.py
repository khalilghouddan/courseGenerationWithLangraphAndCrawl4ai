### Mermaid Generator Node

#Responsibilities:
#- Generate a Mermaid diagram if the lesson requires one.

from langchain_core.runnables import Runnable
from app.models.state import CourseState
from app.services.llm import get_llm
from app.utils.helpers import strip_markdown_fences
from app.utils.logger import log_message


def build_mermaid_agent() -> Runnable:

    def mermaid_node(state: CourseState) -> CourseState:
        lesson = getattr(state, "current_lesson_plan", {})
        mermaid_description = getattr(state, "mermaid_description", "")
        lesson_title = lesson.get("title", "")

        system_prompt = f"""
You are an expert Mermaid diagram generator.

Generate a Mermaid diagram based on the following description.
Only output the valid Mermaid code. Do not include markdown formatting or backticks, just the code itself.

Description:
{mermaid_description}
"""

        with log_message("MERMAID", "#FF4081", f"Generating diagram for: '{lesson_title}'"):
            response = get_llm().invoke(system_prompt)

        mermaid_code = strip_markdown_fences(response.content)
        #strip "mermaid" language tag if present after fence removal
        if mermaid_code.startswith("mermaid"):
            mermaid_code = mermaid_code[len("mermaid"):].strip()

        markdown_diagram = f"\n\n```mermaid\n{mermaid_code}\n```\n\n"

        with log_message("MERMAID", "#FF4081", f"Diagram generated ({len(mermaid_code)} chars) — appending to lesson"):
            if "content_markdown" in lesson:
                lesson["content_markdown"] += markdown_diagram

            if hasattr(state, "generated_lesson") and state.generated_lesson is not None:
                if "content_markdown" in state.generated_lesson:
                    state.generated_lesson["content_markdown"] += markdown_diagram

            state.current_lesson_plan = lesson

        return state

    return mermaid_node


mermaid_node = build_mermaid_agent()
