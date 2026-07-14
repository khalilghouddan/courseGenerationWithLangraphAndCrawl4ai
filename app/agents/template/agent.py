### Template Selection Agent

# Responsibilities:
#- Retrieve candidate templates matching the course language.

#couse data inall graph
from app.models.state import CourseState
from app.agents.template.selector import (
    get_templates_by_language,
    get_template_by_id,
)
from app.agents.template.prompt import build_template_prompt
from app.services.llm import get_llm


async def template_agent(state: CourseState) -> CourseState:

 
    metadata = state.metadata

    if metadata is None:
        raise ValueError("Metadata must be generated before selecting a template.")


    templates = get_templates_by_language(metadata.language)

    if not templates:
        raise ValueError(
            f"No templates found for language '{metadata.language}'."
        )


    prompt = build_template_prompt(
        metadata=metadata,
        templates=templates,
    )


    llm = get_llm()

    response = await llm.ainvoke(prompt)

    selected_template_id = int(response.content.strip())

    # ------------------------------------------------------------------
    # Step 5: Retrieve selected template
    # ------------------------------------------------------------------

    selected_template = get_template_by_id(selected_template_id)

    if selected_template is None:
        raise ValueError(
            f"Template '{selected_template_id}' does not exist."
        )

    # ------------------------------------------------------------------
    # Step 6: Update shared state
    # ------------------------------------------------------------------

    state.template_id = selected_template.id
    state.template = selected_template

    return state