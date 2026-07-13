


#python build in module to calculate time to generate course 
import time
#fast api instance APiRouter : to define the main api / HTTPExaption :handel HTTP error and return responce to client 
from fastapi import APIRouter, HTTPException
#import 
from app.graphs.main_graph import main_graph 
#import 
from app.models.course import CourseRequest, CourseResponse
#import fuction that saves the courses into db 
from app.db.db_ops import save_course, get_all_courses, get_course_by_id
#json module to handel json data in python
import json







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

#async fuction to call the main graph and generate the course and return the response to client
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

        course = result["course"]

        # Save generated course
        db_id = None
        try:
            db_id = save_course(
                course=course,
                generation_time_s=generation_time,
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
    





@router.get("", summary="Get all courses", description="Retrieve basic information for all generated courses.")
async def list_courses():
    try:
        courses = get_all_courses()
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{course_id}", summary="Get course by ID", description="Retrieve the full structured details of a course by its database ID.")
async def retrieve_course(course_id: int):
    try:
        course = get_course_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Deserialise the realcoursebody JSON string if it is stored as a string
        if "realcoursebody" in course and isinstance(course["realcoursebody"], str):
            try:
                course["realcoursebody"] = json.loads(course["realcoursebody"])
            except Exception as parse_err:
                print(f"Failed to parse realcoursebody JSON: {parse_err}")
                
        # Unwrap nested realcoursebody if it was stored with the double-serialization bug
        if "realcoursebody" in course and isinstance(course["realcoursebody"], dict):
            body = course["realcoursebody"]
            while isinstance(body, dict) and "realcoursebody" in body and not ("chapters" in body or "sections" in body):
                body = body["realcoursebody"]
            course["realcoursebody"] = body

        return course
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
