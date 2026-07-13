### CourseState THE BIG BAGPACK

#Responsibilities:
#- This model is used evry node can read from it and write into it

#TODO: seper this file to evry node if it is better 


#imports dateime to define variable 
from datetime import datetime
#
from typing import Any
#obvias pydantic to create a model python 
from pydantic import BaseModel, Field


class CourseState(BaseModel):

    prompt: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    template: dict[str, Any] = Field(default_factory=dict)
    realcoursebody: dict[str, Any] = Field(default_factory=dict)
    urls_scraped: list[str] = Field(default_factory=list)
    structured_response: dict[str, Any] = Field(default_factory=dict)
    generation_time: float = 0.0
    started_at: datetime | None = None
    completed_at: datetime | None = None

    class Config:
        title = "CourseState"
        anystr_strip_whitespace = True
        extra = "ignore"