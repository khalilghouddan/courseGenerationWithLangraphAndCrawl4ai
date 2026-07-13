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
    """
    Select the best course template based on the generated metadata.

    Workflow:
        1. Read metadata from the shared state.
        2. Retrieve templates matching the metadata language.
        3. Build the LLM prompt.
        4. Ask the LLM to select the best template.
        5. Retrieve the selected template.
        6. Store the result in the state.
    """

    # ------------------------------------------------------------------
    # Step 1: Read metadata
    # ------------------------------------------------------------------

    metadata = state.metadata

    if metadata is None:
        raise ValueError("Metadata must be generated before selecting a template.")

    # ------------------------------------------------------------------
    # Step 2: Load candidate templates
    # ------------------------------------------------------------------

    templates = get_templates_by_language(metadata.language)

    if not templates:
        raise ValueError(
            f"No templates found for language '{metadata.language}'."
        )

    # ------------------------------------------------------------------
    # Step 3: Build prompt
    # ------------------------------------------------------------------

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