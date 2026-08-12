from fastapi import FastAPI
from app.routers.resume import router as resume_router
from app.routers.interview import router as interview_router 

app = FastAPI()

app.include_router(resume_router)
app.include_router(interview_router)
@app.get('/')
def root():
    return {"message": "Server Started"}
