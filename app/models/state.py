


from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class CourseState(BaseModel):
    prompt: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    template: dict[str, Any] = Field(default_factory=dict)
    course: Any | None = None
    realcoursebody: dict[str, Any] = Field(default_factory=dict)
    urls_scraped: list[str] = Field(default_factory=list)
    structured_response: dict[str, Any] = Field(default_factory=dict)
    generation_time: float = 0.0
    started_at: datetime | None = None
    completed_at: datetime | None = None
    research_complete: bool = False
    lesson_requires_mermaid: bool = False
    has_next_lesson: bool = True
    current_chapter: int = 0
    current_lesson: int = 0
    current_lesson_plan: dict[str, Any] = Field(default_factory=dict)
    current_research: list[str] = Field(default_factory=list)
    current_sources: list[str] = Field(default_factory=list)
    research_attempts: int = 0
    mermaid_description: str = ""

    model_config = {
        "title": "CourseState",
        "str_strip_whitespace": True,
        "extra": "ignore",
    }