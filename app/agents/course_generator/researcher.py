"""
Researcher Node

Responsibilities:
- Generate search queries for the current lesson.
- Search the web.
- Scrape relevant pages.
- Evaluate whether enough information has been collected.
- Retry with refined queries when necessary.
"""

from typing import List

from app.models.state import CourseState

from app.tools.web_search import search_web
from app.tools.scraper import scrape_urls

from app.services.llm import get_llm


MAX_RESEARCH_ATTEMPTS = 3


def _generate_queries(
    llm,
    title: str,
    objective: str,
    previous_sources: List[str],
) -> List[str]:
    """
    Ask the LLM to generate search queries.
    """

    prompt = f"""
Lesson title:
{title}

Learning objective:
{objective}

Previous sources:
{previous_sources}

Generate 5 high-quality search queries.
Only return one query per line.
"""

    response = llm.invoke(prompt)

    return [
        line.strip()
        for line in response.content.splitlines()
        if line.strip()
    ]


def _evaluate_research(
    llm,
    title: str,
    objective: str,
    documents: List[str],
) -> bool:
    """
    Ask the LLM if enough information exists
    to write the lesson.
    """

    prompt = f"""
Lesson:
{title}

Objective:
{objective}

Collected information:

{documents[:10]}

Can a complete lesson be written?

Answer only:

YES

or

NO
"""

    response = llm.invoke(prompt)

    return "YES" in response.content.upper()


def researcher_node(state: CourseState) -> CourseState:
    """
    Research the current lesson.
    """

    llm = get_llm()

    lesson = getattr(state, "current_lesson_plan", {})

    title = lesson.get("title", "")
    objective = lesson.get("goal", "")

    collected_documents = []

    previous_sources = []

    while state.research_attempts < MAX_RESEARCH_ATTEMPTS:

        queries = _generate_queries(
            llm,
            title,
            objective,
            previous_sources,
        )

        urls = search_web(queries)

        documents = scrape_urls(urls)

        collected_documents.extend(documents)

        previous_sources.extend(urls)

        enough = _evaluate_research(
            llm,
            title,
            objective,
            collected_documents,
        )

        if enough:

            state.current_research = collected_documents
            state.current_sources = previous_sources

            state.research_complete = True
            state.research_attempts = 0

            return state

        state.research_attempts += 1

    state.current_research = collected_documents
    state.current_sources = previous_sources

    state.research_complete = True

    state.research_attempts = 0

    return state