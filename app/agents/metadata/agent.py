###Metadata Agent

#Responsibilities:
#- Understand the user propt
#- Generate the metadata of the course 


#
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from app.agents.metadata.models import CourseMetadata
from app.agents.metadata.prompt import METADATA_PROMPT

from app.services.llm import get_llm


def build_metadata_agent() -> Runnable:
   

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