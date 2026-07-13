"""
Metadata Agent

This agent analyzes the user's prompt and extracts structured metadata
that will be used by the Template Agent and the Course Content Agent.

Responsibilities:
- Understand the user's learning goal
- Determine difficulty level
- Estimate course duration
- Identify prerequisites
- Generate learning objectives
- Extract main topics
"""

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from app.agents.metadata.models import CourseMetadata
from app.agents.metadata.prompt import METADATA_PROMPT

from app.services.llm import get_llm


def build_metadata_agent() -> Runnable:
    """
    Build the Metadata Agent.

    Returns:
        Runnable LangChain pipeline.
    """

    parser = PydanticOutputParser(pydantic_object=CourseMetadata)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", METADATA_PROMPT),
            (
                "human",
                "User Request:\n{user_prompt}\n\n"
                "{format_instructions}",
            ),
        ]
    ).partial(
        format_instructions=parser.get_format_instructions()
    )

    llm = get_llm()

    metadata_agent = (
        prompt
        | llm
        | parser
    )

    return metadata_agent