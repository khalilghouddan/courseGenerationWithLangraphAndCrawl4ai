#Template Selection Agent.

#Responsibilities:
#- Analyze the generated metadata.
#- Select the most appropriate course template.


from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser

from app.models.state import CourseState
from app.models.metadata import CourseMetadata
from app.schemas.template_schema import TemplateSelection
from app.services.llm import get_llm
from app.agents.template.prompt import TEMPLATE_SELECTION_PROMPT


async def template_agent(state: CourseState) -> CourseState:

    # Extract metadata
    metadata: CourseMetadata = state.metadata

    llm = get_llm()

    parser = JsonOutputParser(pydantic_object=TemplateSelection)

    chain = (
        TEMPLATE_SELECTION_PROMPT
        | llm
        | parser
    )

    result = await chain.ainvoke(
        {
            "title": metadata.title,
            "subject": metadata.subject,
            "difficulty": metadata.difficulty,
            "duration": metadata.duration,
            "language": metadata.language,
            "learning_style": metadata.learning_style,
            "goal": metadata.goal,
            "topics": metadata.topics,
            "format_instructions": parser.get_format_instructions(),
        }
    )

    state.template = result

    return state