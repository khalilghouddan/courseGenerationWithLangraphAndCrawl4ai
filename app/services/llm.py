### Service LLMs 
# connection with open ai 
# multiple modes 


#retun a an open ai chat with spasefic configuration like tempeture and model name
from langchain_openai import ChatOpenAI
#setting from settings file
from app.utils.config import settings

#mother fuction that return a chat open ai with spesefic configuration
def get_llm(model: str | None = None,temperature: float = 0.2,) -> ChatOpenAI:

    return ChatOpenAI(
        model=model or settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

#chosing the fast one hihihihi
def get_fast_llm() -> ChatOpenAI:
    
    return get_llm(
        model=settings.OPENAI_MODEL_FAST,
    )


def get_balanced_llm() -> ChatOpenAI:
   
    return get_llm(
        model=settings.OPENAI_MODEL_BALANCED,
    )


def get_reasoning_llm() -> ChatOpenAI:
    
    return get_llm(
        model=settings.OPENAI_MODEL_REASONING,
    )