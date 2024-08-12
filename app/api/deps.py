from fastapi import Request, HTTPException
import logging

logger = logging.getLogger(__name__)

async def get_current_user(request: Request):
    if not request.state.user:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")
    return request.state.user
