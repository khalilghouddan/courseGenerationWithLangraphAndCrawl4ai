### The MAIN 
# gadring the apis 
# starting the front end 


#fastapi thz main object to create the API 
from fastapi import FastAPI
#import midelware to allow cross-origin request originr from the frontend
#creoss cross-origin resource sharing (CORS) is a security origines means port 8000 9000 the backend must allow it 
from fastapi.middleware.cors import CORSMiddleware
#to allow the server to serve stic files like index.hrml and main.js ....
from fastapi.staticfiles import StaticFiles
#python operating system module to handel file path and derectory 
import os
#import all routes from the file api 
from app.api.courseGeneration import router as course_router
from app.api.docs import router as docs_router
from app.api.frontEndApis import router as frontend_router
from app.api.health import router as health_router

#create the main api object 
app = FastAPI(
    #big tile
    title="DeepAgent Course Generator API",
    #short description
    description=(
        "API for generating structured courses and inspecting service health. "
        "Interactive docs are available at `/docs` and `/redoc`."
    ),
    version="2.0.0"
)

# Allow the React frontend (served on same host or different port) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(course_router)
app.include_router(frontend_router)
app.include_router(health_router)
app.include_router(docs_router)



# Serve the React frontend from /app
#frontend_dir is the path to the frontend directory 
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
#check if the frontend exist 
if os.path.isdir(frontend_dir):
    #mount means to serve the static files from the frontend directory at the /app endpoint
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")



#run the fast api server using uvicorn 
if __name__ == "__main__":
    #import uvicorn a lightweight ASGI server for running FastAPI applications in development and production environments. 
    import uvicorn
    #start ASGI server with app object 
    uvicorn.run("app.main:app", host="0.0.0.0", port=8011, reload=True)
