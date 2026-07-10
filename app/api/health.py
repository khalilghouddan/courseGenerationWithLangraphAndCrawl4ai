


#
import asyncio

from fastapi import APIRouter

from app.db.chekes import check_db, check_search, check_crawl, check_llm

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Checks database, Search API, Crawl API, and LLM connectivity.",
)
async def health_check():
    db_task = asyncio.to_thread(check_db)
    search_task = asyncio.to_thread(check_search)
    crawl_task = asyncio.to_thread(check_crawl)
    llm_task = asyncio.to_thread(check_llm)

    (db_status, db_err), (search_status, search_err), (crawl_status, crawl_err), (llm_status, llm_err) = await asyncio.gather(
        db_task, search_task, crawl_task, llm_task
    )

    is_healthy = all(
        status == "up"
        for status in [db_status, search_status, crawl_status, llm_status]
    )

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "services": {
            "db":       {"status": db_status,  "error": db_err},
            "searxng":  {"status": search_status,  "error": search_err},
            "crawl4ai": {"status": crawl_status,  "error": crawl_err},
            "llm":      {"status": llm_status,  "error": llm_err},
        },
    }
