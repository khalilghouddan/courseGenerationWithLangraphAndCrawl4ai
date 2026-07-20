from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CourseRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class CourseOutput(BaseModel):
    title: str
    headline: str
    description: str
    objectives: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    target_audiences: str
    primary_category_title: str
    primary_subcategory_title: str
    duration: str
    language: str = "English"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    urls_scraped: list[str] = Field(default_factory=list)
    realcoursebody: dict[str, Any] = Field(default_factory=dict)


class CourseResponse(BaseModel):
    success: bool
    id: int | None = None
    generation_time: float
    course: CourseOutput
