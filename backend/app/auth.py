import os

from fastapi import HTTPException, Request
from clerk_backend_api import AuthenticateRequestOptions, authenticate_request


def require_auth(request: Request):
    state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=os.environ["CLERK_SECRET_KEY"],
            authorized_parties=[os.environ["FRONTEND_URL"]],
            accepts_token=["session_token"],
        ),
    )

    if not state.is_authenticated:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return state