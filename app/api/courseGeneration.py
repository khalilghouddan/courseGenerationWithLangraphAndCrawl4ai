
# Python built-in module to calculate time to generate course
import time
from datetime import datetime

# FastAPI: APIRouter to define routes, HTTPException to return HTTP errors
from fastapi import APIRouter, HTTPException

# Main LangGraph workflow
from app.graphs.main_graph import main_graph

# Request / response models
from app.models.course import CourseOutput, CourseRequest, CourseResponse

# DB helper
from app.db.coursDB import save_course







#define the prefix routes (all routes start with /courses and tag them for documentation)
router = APIRouter(prefix="/courses", tags=["Courses"])


#decorator of fuction define the post endpoint 
@router.post(
    #/courses/generate
    "/generate",
    #short fucking description for swager docs
    summary="Generate a course",
    #long description for swager docs
    description=(
        "Runs the course-generation agent, which researches the topic, selects a template, "
        "and returns a structured course record."
    ),
)

#async function to call the main graph and generate the course and return the response to client
async def generate_course(request: CourseRequest) -> CourseResponse:
   
    try:
        # Measure generation time
        start_time = time.time()

        # Execute the LangGraph workflow
        result = await main_graph.ainvoke(
            {
                "prompt": request.prompt,
            }
        )

        generation_time = time.time() - start_time

        # ── Assemble CourseOutput from the finished state ──────────────────
        # The graph never writes state.course — the completed course lives in:
        #   result["template"]  → full chapter/lesson body (realcoursebody)
        #   result["metadata"]  → title, description, objectives, …
        metadata: dict = result.get("metadata", {})
        template: dict = result.get("template", {})
        urls_scraped: list = result.get("current_sources", [])

        course = CourseOutput(
            title=metadata.get("title", ""),
            headline=metadata.get("headline", ""),
            description=metadata.get("description", ""),
            objectives=metadata.get("objectives", []),
            prerequisites=metadata.get("prerequisites", []),
            target_audiences=metadata.get("target_audiences", ""),
            primary_category_title=metadata.get("primary_category_title", ""),
            primary_subcategory_title=metadata.get("primary_subcategory_title", ""),
            duration=metadata.get("duration", ""),
            language=metadata.get("language", "English"),
            created_at=datetime.utcnow(),
            urls_scraped=urls_scraped,
            realcoursebody=template,
        )
        # ──────────────────────────────────────────────────────────────────

        # Save generated course
        db_id = None
        try:
            db_id = save_course(
                course=course,
                generation_time_s=generation_time,
                urls_used=urls_scraped,
            )
        except Exception as db_error:
            # Don't fail the API if the database save fails
            print(f"Database save failed: {db_error}")

        # Return response
        return CourseResponse(
            success=True,
            id=db_id,
            generation_time=generation_time,
            course=course,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Course generation failed: {str(e)}",
        )
    
