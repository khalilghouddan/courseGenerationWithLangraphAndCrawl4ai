### Course Researcher Agent

#Responsibilities:
#- Generate search queries for the current lesson via query_builder.
#- Search the web.
#- Scrape relevant pages.
#- Evaluate whether enough information has been collected.
#- Retry with refined queries when necessary.

from typing import List

from app.models.state import CourseState
from app.tools.web_search import search_web
from app.tools.scraper import scrape_urls
from app.services.llm import get_llm
from app.utils.logger import log_message, log_info
from app.agents.course_generator.query_builder import build_search_queries, resolve_subject


MAX_RESEARCH_ATTEMPTS = 3


def _evaluate_research(
    llm,
    title: str,
    objective: str,
    documents: List[str],
) -> bool:
    """Ask the LLM if enough information exists to write the lesson."""

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
    with log_message("RESEARCHER", "#00BCD4", f"Evaluating research sufficiency for: '{title}'"):
        response = llm.invoke(prompt)

    return "YES" in response.content.upper()


def researcher_node(state: CourseState) -> CourseState:

    llm = get_llm()

    lesson = getattr(state, "current_lesson_plan", {})
    metadata = state.metadata

    #extract the real subject from metadata to resolve [SUBJECT] placeholders
    subject = metadata.get("primary_subcategory_title") or metadata.get("title", "the subject")
    course_title = metadata.get("title", "")

    raw_title = lesson.get("title", "")
    raw_objective = lesson.get("goal", "")

    #resolved versions (no [SUBJECT] placeholder)
    resolved_title = resolve_subject(raw_title, subject)
    resolved_objective = resolve_subject(raw_objective, subject)

    with log_message(
        "RESEARCHER",
        "#00BCD4",
        f"Starting research | Chapter {state.current_chapter} Lesson {state.current_lesson} | '{resolved_title}'",
    ):
        collected_documents = []
        previous_sources = []

        while state.research_attempts < MAX_RESEARCH_ATTEMPTS:

            #use query_builder to generate focused, placeholder-free queries
            queries = build_search_queries(
                lesson_title=raw_title,
                lesson_objective=raw_objective,
                subject=subject,
                course_title=course_title,
                previous_sources=previous_sources,
            )

            with log_message(
                "RESEARCHER",
                "#00BCD4",
                f"Attempt {state.research_attempts + 1}/{MAX_RESEARCH_ATTEMPTS} | Searching web with {len(queries)} queries",
            ):
                urls = search_web(queries)
                documents = scrape_urls(urls)

            collected_documents.extend(documents)
            previous_sources.extend(urls)

            log_info("RESEARCHER", "#00BCD4", f"Scraped {len(documents)} documents | Total so far: {len(collected_documents)}")

            enough = _evaluate_research(llm, resolved_title, resolved_objective, collected_documents)

            if enough:
                with log_message("RESEARCHER", "#00BCD4", f"Research complete after {state.research_attempts + 1} attempt(s)"):
                    state.current_research = collected_documents
                    state.current_sources = previous_sources
                    state.research_complete = True
                    state.research_attempts = 0
                return state

            state.research_attempts += 1

        with log_message("RESEARCHER", "#00BCD4", f"Max attempts reached ({MAX_RESEARCH_ATTEMPTS}) — proceeding with available data"):
            state.current_research = collected_documents
            state.current_sources = previous_sources
            state.research_complete = True
            state.research_attempts = 0

    return state