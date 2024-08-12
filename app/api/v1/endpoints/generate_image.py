from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.utils.openai_utils import generateImage
import logging
from app.config import Config
import openai
from fastapi.security import HTTPBearer
from app.api.schemas import ImageRequest
from app.utils.challenge_utils import get_descriptive_participation_type , get_descriptive_result_type
logger = logging.getLogger(__name__)

router = APIRouter()

# Create security instance
security = HTTPBearer()

@router.post("/", dependencies=[Depends(security)], tags=["generate-image"])
async def generate_image(request: ImageRequest, http_request: Request, user: dict = Depends(get_current_user)):
    user_id = user.get("userId")

    # Handle default values for optional fields
    descriptive_participation = get_descriptive_participation_type(request.participation_type.value) if request.participation_type else "unspecified competition type"
    descriptive_result = get_descriptive_result_type(request.result_type.value) if request.result_type else "unspecified result determination method"

    if not request.prompt:
        logger.error(f"User ID: {user_id} - Prompt is required but not provided")
        raise HTTPException(status_code=400, detail="Prompt is required.")

    prompt_text = f"Generate a Image based on the following prompt: {request.prompt}. This is a {descriptive_participation} and the challenge results are {descriptive_result}. Additional info: {request.additional_info if request.additional_info else 'No additional info provided'}. Do not add any text in the image"

    try:
        image_url = generateImage(Config.OPENAI_API_KEY, prompt_text)
        if image_url:
            logger.info(f"User ID: {user_id} - Image generated: {image_url}")
            return {"image_url": image_url,
                    "participation_type" : descriptive_participation, 
                    "result_type" : descriptive_result,
                    "additional_info" : request.additional_info
            }
        else:
            logger.error(f"User ID: {user_id} - Failed to generate image")
            raise HTTPException(status_code=500, detail="Failed to generate image.")
    except openai.error.OpenAIError as e:
        logger.error(f"User ID: {user_id} - Exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
