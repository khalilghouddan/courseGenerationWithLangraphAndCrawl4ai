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
import json


from app.models.state import CourseState
from app.utils.logger import log_message


def build_metadata_agent() -> Runnable:
   

    parser = PydanticOutputParser(pydantic_object=CourseMetadata)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", METADATA_PROMPT.template),
        ]
    ).partial(
        format_instructions=parser.get_format_instructions()
    )

    llm = get_llm()

    chain = (
        prompt
        | llm
        | parser
    )

    def metadata_agent(state: CourseState) -> CourseState:
        with log_message("METADATA_AGENT", "#00B8D9", f"Invoking metadata LLM "):
            response = chain.invoke({"prompt": state.prompt})
            state.metadata = response.model_dump()
            print(f"\n[Generated Course Metadata]:\n{json.dumps(state.metadata, indent=2)}\n")
            return state

    return metadata_agent