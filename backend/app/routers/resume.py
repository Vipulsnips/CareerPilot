from fastapi import APIRouter, UploadFile, File, Depends

from app.auth import require_auth
from app.services.resume_service import process_resume


router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    auth_state=Depends(require_auth),
):
    user_id = auth_state.payload["sub"]

    return await process_resume(
        file=file,
        user_id=user_id,
    )