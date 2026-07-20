### Template Agent

# Responsibilities:
#- Use the prompt + LLM to intelligently select the best course template
#- based on the course metadata generated in the previous step.


import json

from app.utils.helpers import strip_markdown_fences

from langchain_core.messages import HumanMessage

from app.models.state import CourseState
from app.utils.logger import log_message
from app.services.llm import get_llm
from app.db.templateDB import select_template_by_id
from app.agents.template.selector import get_templates_by_language
from app.agents.template.prompt import build_template_prompt


def select_template(state: CourseState) -> CourseState:

    # Validate that metadata was produced by a previous step
    metadata = state.metadata
    if not metadata:
        raise ValueError("Metadata must be generated before selecting a template.")

    language = metadata.get("language")

    #Fetch candidate templates via selector
    candidates = get_templates_by_language(language)
    if not candidates:
        raise ValueError("No templates found in the database.")

    #Build the prompt and ask the LLM to choose
    # We need a metadata object with attribute access for build_template_prompt
    from types import SimpleNamespace
    meta_ns = SimpleNamespace(
        title=metadata.get("title", ""),
        topic=metadata.get("topic", ""),
        difficulty=metadata.get("difficulty", ""),
        target_audience=metadata.get("target_audience", ""),
        duration=metadata.get("duration", ""),
        learning_goal=metadata.get("learning_goal", ""),
        language=language,
    )

    prompt_text = build_template_prompt(meta_ns, candidates)

    llm = get_llm()

    with log_message("TEMPLATE_AGENT", "#FF9800", "Invoking LLM to select best template"):
        response = llm.invoke([HumanMessage(content=prompt_text)])

    #Parse the LLM response
    raw = strip_markdown_fences(response.content)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON for template selection: {e}\nRaw response: {raw}")

    selected_id = result.get("template_id")
    reason = result.get("reason", "")

    if not selected_id:
        raise ValueError(f"LLM did not return a template_id. Response: {result}")

    # Fetch the full template record from the DB 
    full_template = select_template_by_id(selected_id)
    if not full_template:
        raise ValueError(f"Template with ID '{selected_id}' returned by LLM was not found in the database.")

    state.template = dict(full_template)

    with log_message(
        "TEMPLATE_AGENT",
        "#FF9800",
        f"Selected Template ID: {state.template['id']} |  Selected Template Title: {state.template['title']}  | Selected Template Reason: {reason}",
    ):
        pass

    return state