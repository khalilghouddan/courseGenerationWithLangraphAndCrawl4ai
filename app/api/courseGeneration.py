


#python build in module to calculate time to generate course 
import time
#fast api instance APiRouter : to define the main api / HTTPExaption :handel HTTP error and return responce to client 
from fastapi import APIRouter, HTTPException
#pydantic to validate outcoming and outgoing data BaseModel : to define request responce chema / Field: description and metadata rules
from pydantic import BaseModel, Field
#part of langchain to send messsgaes obect from hiuman to agnet 
from langchain_core.messages import HumanMessage, AIMessage
#import deepagnt workflow
from src.agents.workflow import build_workflow
#import course output schema
from src.utiles.schemas import CourseOutput
#import fuction that saves the courses into db 
from src.utiles.db_ops import save_course, get_all_courses, get_course_by_id
from src.utiles.extractor import extraction_function
#json module to handel json data in python
import json

from app.models.course import CourseRequest, CourseResponse
from app.graphs.main_graph import course_graph




#define the prefix routes (all routes start with /courses and tag them for documentation)
router = APIRouter(prefix="/courses", tags=["Courses"])

#define the request schema for cours generation endpoint
#for documentation
class GenerateCourseRequest(BaseModel):
    #there is onefield that is required 
    prompt: str = Field(
        ...,
        #swager docs
        examples=[
            "Create a beginner course about Python programming for absolute beginners."
        ],
        #this is the description shown in the documentaion API docs
        description="Natural-language course request that the agent will turn into a structured course.",
    )

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

async def generate_course(request: CourseRequest) -> CourseResponse:
    """
    Generate a complete course from a user prompt.
    """

    try:
        result = await course_graph.ainvoke(
            {
                "prompt": request.prompt,
            }
        )

        return CourseResponse(
            success=True,
            course=result["course"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
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
