from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
import openai
from app.config import Config
from app.api.deps import get_current_user
from app.utils.openai_utils import generateImage
import logging
from fastapi.security import HTTPBearer
from app.api.schemas import ChallengeDescriptionRequest
from app.utils.challenge_utils import get_descriptive_participation_type,get_descriptive_result_type
logger = logging.getLogger(__name__)

router = APIRouter()

security = HTTPBearer()

# Define a global chat_sessions dictionary
chat_sessions = {}

@router.post("/", dependencies=[Depends(security)], tags=["generate-description"])
async def generate_description(request: ChallengeDescriptionRequest, http_request: Request, user: dict = Depends(get_current_user)):
    user_id = user.get("userId")
    
    # Handle default values for optional fields
    descriptive_participation = get_descriptive_participation_type(request.participation_type.value) if request.participation_type else "unspecified competition type"
    descriptive_result = get_descriptive_result_type(request.result_type.value) if request.result_type else "unspecified result determination method"
    
    prompt_text = f"Generate a challenge title and description based on the following prompt: {request.prompt}. This is a {descriptive_participation} and the challenge results are {descriptive_result}. Additional info: {request.additional_info if request.additional_info else 'No additional info provided'}"

    chat_sessions[user_id] = {
        "openai_model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt_text}],
        "data": {},
        "state": "waiting_for_user_edit"
    }

    try:
        response = openai.ChatCompletion.create(
            model=chat_sessions[user_id]["openai_model"],
            messages=chat_sessions[user_id]["messages"],
            max_tokens=150,
        )
        
        if response.choices:
            response_text = response.choices[0].message['content'].split('\n', 1)
            challenge_name = response_text[0].replace("Title: ", "").strip()
            challenge_description = response_text[1].replace("Description: ", "").strip()

            # Remove leading and trailing double quotes if present
            if challenge_name.startswith('"') and challenge_name.endswith('"'):
                challenge_name = challenge_name[1:-1]
            if challenge_description.startswith('"') and challenge_description.endswith('"'):
                challenge_description = challenge_description[1:-1]

            chat_sessions[user_id]["data"]["name"] = challenge_name
            chat_sessions[user_id]["data"]["description"] = challenge_description

            image_url = generateImage(Config.OPENAI_API_KEY, request.prompt)
            chat_sessions[user_id]["data"]["image_url"] = image_url if image_url else "No image generated."

            logger.info(f"User ID: {user_id} - Challenge generated: {challenge_name} - {challenge_description}")

            return {
                "challenge_title": challenge_name,
                "challenge_description": challenge_description,
                "participation_type": descriptive_participation,
                "result_type": descriptive_result,
                "additional_info": request.additional_info
            }
        else:
            logger.error(f"User ID: {user_id} - Failed to fetch a response from OpenAI")
            raise HTTPException(status_code=500, detail="Sorry, I couldn't fetch a response.")
    except openai.error.OpenAIError as e:
        logger.error(f"User ID: {user_id} - Exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
