
import json

from fastapi import APIRouter, HTTPException

from app.db.coursDB import get_all_courses, get_course_by_id

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", summary="Get all courses", description="Retrieve basic information for all generated courses.")
async def list_courses():
    try:
        return get_all_courses()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/{course_id}", summary="Get course by ID", description="Retrieve the full structured details of a course by its database ID.")
async def retrieve_course(course_id: int):
    try:
        course = get_course_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        if "realcoursebody" in course and isinstance(course["realcoursebody"], str):
            try:
                course["realcoursebody"] = json.loads(course["realcoursebody"])
            except Exception as parse_err:
                print(f"Failed to parse realcoursebody JSON: {parse_err}")

        if "realcoursebody" in course and isinstance(course["realcoursebody"], dict):
            body = course["realcoursebody"]
            while isinstance(body, dict) and "realcoursebody" in body and not ("chapters" in body or "sections" in body):
                body = body["realcoursebody"]
            course["realcoursebody"] = body

        return course
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
