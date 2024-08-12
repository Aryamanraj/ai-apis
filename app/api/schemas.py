from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class ParticipationType(str, Enum):
    dare = "0v1"
    challenge = "1v1"
    community = "NvN"

class ResultType(str, Enum):
    steps = "steps"
    calories = "calories"
    validator = "validator"
    voting = "voting"
    reclaim = "reclaim"

class ChallengeDescriptionRequest(BaseModel):
    prompt: str
    participation_type: Optional[ParticipationType] = Field(None, description="Choose the type of participation for the challenge")
    result_type: Optional[ResultType] = Field(None, description="Choose the result determination method for the challenge")
    additional_info: Optional[str] = Field(None, description="Any additional information relevant to the challenge")

class ImageRequest(BaseModel):
    prompt: str
    participation_type: Optional[ParticipationType] = Field(None, description="Choose the type of participation for the challenge")
    result_type: Optional[ResultType] = Field(None, description="Choose the result determination method for the challenge")
    additional_info: Optional[str] = Field(None, description="Any additional information relevant to the challenge")

class User(BaseModel):
    username: str
    password: str
