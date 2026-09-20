from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.exceptions import GeminiServiceError, LLMResponseValidationError
from app.routers.resume import router as resume_router
from app.routers.interview import router as interview_router
from app.routers.evaluation import router as evaluation_router
from app.logging_config import logger
from app.routers.rag import router as rag_router

app = FastAPI()


@app.exception_handler(GeminiServiceError)
async def gemini_service_error_handler(
    request: Request,
    exc: GeminiServiceError,
):
    logger.exception(
        "Gemini service error",
        extra={"event": "gemini_service_error"},
    )

    return JSONResponse(
        status_code=503,
        content={"detail": "AI service temporarily unavailable"},
    )


@app.exception_handler(LLMResponseValidationError)
async def llm_response_validation_error_handler(
    request: Request,
    exc: LLMResponseValidationError,
):
    logger.exception(
        "LLM response validation failed",
        extra={"event": "llm_response_validation_error"},
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "AI response could not be processed"},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(evaluation_router)
app.include_router(rag_router)


@app.get("/")
def root():
    return {"message": "Server Started"}
