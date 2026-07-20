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
        model=model or settings.QUEN_MODEL,
        api_key=settings.MODEL_API_KEY,
        base_url=settings.MODEL_BASE_URL,
    )

#chosing the fast one hihihihi
def get_fast_llm() -> ChatOpenAI:
    
    return get_llm(
        model=settings.QUEN_MODEL,
    )


def get_balanced_llm() -> ChatOpenAI:
   
    return get_llm(
        model=settings.MISTRAL_MODEL,
    )


def get_reasoning_llm() -> ChatOpenAI:
    
    return get_llm(
        model=settings.QUEN_MODEL,
    )