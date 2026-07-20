### Mermaid Generator Node

# Responsibilities:
# - Generate a Mermaid diagram if the lesson requires one.

from langchain_core.runnables import Runnable
from app.models.state import CourseState
from app.services.llm import get_llm
from app.utils.helpers import strip_markdown_fences


def build_mermaid_agent() -> Runnable:
    """
    Build the Mermaid agent.
    """

    def mermaid_node(state: CourseState) -> CourseState:
        lesson = getattr(state, "current_lesson_plan", {})
        mermaid_description = getattr(state, "mermaid_description", "")
        
        system_prompt = f"""
You are an expert Mermaid diagram generator.

Generate a Mermaid diagram based on the following description.
Only output the valid Mermaid code. Do not include markdown formatting or backticks, just the code itself.

Description:
{mermaid_description}
"""
        
        # Use LLM to generate the diagram code
        response = get_llm().invoke(system_prompt)
        mermaid_code = strip_markdown_fences(response.content)
        #strip "mermaid" language tag if present after fence removal
        if mermaid_code.startswith("mermaid"):
            mermaid_code = mermaid_code[len("mermaid"):].strip()

        # Format as markdown block
        markdown_diagram = f"\n\n```mermaid\n{mermaid_code}\n```\n\n"
        
        # Append to the lesson markdown
        if "content_markdown" in lesson:
            lesson["content_markdown"] += markdown_diagram
            
        # The formatter_node might use generated_lesson depending on how it's called
        if hasattr(state, "generated_lesson") and state.generated_lesson is not None:
            if "content_markdown" in state.generated_lesson:
                state.generated_lesson["content_markdown"] += markdown_diagram

        state.current_lesson_plan = lesson
        return state

    return mermaid_node


mermaid_node = build_mermaid_agent()
