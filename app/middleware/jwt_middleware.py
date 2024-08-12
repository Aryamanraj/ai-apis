from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.security import verify_jwt
import logging

logger = logging.getLogger(__name__)

async def jwt_middleware(request: Request, call_next):
    auth_header = request.headers.get("authorization")
    if auth_header:
        token = auth_header.split(" ")[1] if " " in auth_header else auth_header
        try:
            request.state.user = verify_jwt(token)
        except HTTPException as e:
            logger.error(f"JWT authentication failed: {e.detail}, IP: {request.client.host}, Headers: {dict(request.headers)}")
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    else:
        logger.error(f"Missing JWT token, IP: {request.client.host}, Headers: {dict(request.headers)}")
        request.state.user = None
    response = await call_next(request)
    return response
