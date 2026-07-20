### Course Researcher Agent

# Responsibilities:
# - Generate search queries for the current lesson via query_builder.
# - Search the web.
# - Scrape relevant pages (async — never blocks the event loop).
# - Pass all collected documents to the writer (no evaluation step).

from app.models.state import CourseState
from app.tools.web_search import search_web_async
from app.tools.scraper import scrape_urls_async
from app.utils.logger import log_message, log_info
from app.agents.course_generator.query_builder import build_search_queries, resolve_subject


async def researcher_node(state: CourseState) -> CourseState:

    lesson = getattr(state, "current_lesson_plan", {})
    metadata = state.metadata

    # Extract the real subject to resolve [SUBJECT] placeholders
    subject = metadata.get("primary_subcategory_title") or metadata.get("title", "the subject")
    course_title = metadata.get("title", "")

    raw_title = lesson.get("title", "")
    raw_objective = lesson.get("goal", "")

    resolved_title = resolve_subject(raw_title, subject)

    # Language ISO code for SearXNG
    lang_map = {"Spanish": "es", "French": "fr", "Arabic": "ar", "English": "en"}
    lang_code = lang_map.get(metadata.get("language", "English"), "en")

    with log_message(
        "RESEARCHER",
        "#00BCD4",
        f"Starting research | Chapter {state.current_chapter} Lesson {state.current_lesson} | '{resolved_title}'",
    ):
        # Build 3 focused queries (sync LLM call — fast, ~1-2s)
        queries = build_search_queries(
            lesson_title=raw_title,
            lesson_objective=raw_objective,
            subject=subject,
            course_title=course_title,
            previous_sources=[],
            language=metadata.get("language", "English"),
        )

        # Search (async — does not block the event loop)
        with log_message("RESEARCHER", "#00BCD4", f"Searching web with {len(queries)} queries"):
            urls = await search_web_async(queries, language=lang_code)

        if urls:
            log_info("RESEARCHER", "#00BCD4", f"URLs to scrape ({len(urls)}):")
            for url in urls:
                log_info("RESEARCHER", "#00BCD4", f"  -> {url}")
            # Scrape async — batches run concurrently, 30s hard timeout per batch
            documents = await scrape_urls_async(urls)
        else:
            log_info("RESEARCHER", "#00BCD4", "No URLs returned by search")
            documents = []

        log_info("RESEARCHER", "#00BCD4", f"Scraped {len(documents)} documents")

        state.current_research = documents
        state.current_sources = urls
        state.research_complete = True
        state.research_attempts = 0

    return state