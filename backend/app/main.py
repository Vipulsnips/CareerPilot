from fastapi import FastAPI
from app.routers.resume import router as resume_router

app = FastAPI()

app.include_router(resume_router)

@app.get('/')
def root():
    return {"message": "Server Started"}
