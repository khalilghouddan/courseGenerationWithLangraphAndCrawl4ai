import time

from fastapi import APIRouter, HTTPException

from app.db.coursDB import save_course
from app.graphs.main_graph import main_graph
from app.models.course import CourseRequest, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post(
    "/generate",
    summary="Generate a course",
    description="Runs the course-generation workflow and returns a structured course record.",
)
async def generate_course(request: CourseRequest) -> CourseResponse:
    try:
        start_time = time.time()
        result = await main_graph.ainvoke({"prompt": request.prompt})
        generation_time = time.time() - start_time

        course = result.get("course")
        if course is None:
            raise ValueError("Course generation did not produce a course output")

        db_id = None
        try:
            db_id = save_course(course=course, generation_time_s=generation_time)
        except Exception as db_error:
            print(f"Database save failed: {db_error}")

        return CourseResponse(
            success=True,
            id=db_id,
            generation_time=generation_time,
            course=course,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Course generation failed: {exc}") from exc
