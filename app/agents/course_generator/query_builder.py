### Query Builder

#Responsibilities:
#- Resolve [SUBJECT] placeholders in lesson titles using the real course subject.
#- Ask the LLM to generate focused, high-quality search queries for a lesson.

from typing import List
from pydantic import BaseModel, Field

from app.services.llm import get_llm
from app.utils.logger import log_message, log_info


#structured output – guarantees exactly N clean query strings
class SearchQueries(BaseModel):
    queries: List[str] = Field(
        description="List of 5 focused web search queries for the lesson. No placeholders like [SUBJECT]."
    )


def resolve_subject(text: str, subject: str) -> str:
    """Replace the [SUBJECT] template placeholder with the real subject."""
    return text.replace("[SUBJECT]", subject)


def build_search_queries(
    lesson_title: str,
    lesson_objective: str,
    subject: str,
    course_title: str,
    previous_sources: List[str],
) -> List[str]:
    """
    Generate 5 focused search queries for a lesson.

    [SUBJECT] placeholders are resolved before the LLM sees them so
    queries are always about the real topic (e.g. Python, not [SUBJECT]).

    Args:
        lesson_title:      Raw lesson title (may contain [SUBJECT]).
        lesson_objective:  Raw lesson objective/goal (may contain [SUBJECT]).
        subject:           The real subject extracted from course metadata
                           (e.g. "Python", "Database Design").
        course_title:      Full course title for extra context.
        previous_sources:  URLs already used so the LLM can avoid them.

    Returns:
        List of search query strings.
    """
    #resolve placeholders
    resolved_title = resolve_subject(lesson_title, subject)
    resolved_objective = resolve_subject(lesson_objective, subject)

    log_info("QUERY_BUILDER", "#00BCD4", f"Building queries | subject='{subject}' | lesson='{resolved_title}'")

    prompt = f"""
You are a research assistant helping build an online course about "{subject}".

Course title: {course_title}

You need to find web content for the following lesson:

Lesson title:
{resolved_title}

Learning objective:
{resolved_objective}

Already searched sources (avoid these):
{previous_sources if previous_sources else "None"}

Generate exactly 5 focused, specific web search queries that will find
the best content to write this lesson. Use the real subject name "{subject}"
in every query — never use placeholder text like [SUBJECT].
"""

    with log_message("QUERY_BUILDER", "#00BCD4", f"LLM generating queries for: '{resolved_title}'"):
        response = get_llm().with_structured_output(SearchQueries).invoke(prompt)

    queries = response.queries
    log_info("QUERY_BUILDER", "#00BCD4", f"Generated {len(queries)} queries: {queries}")
    return queries
