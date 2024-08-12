import openai
import logging

logger = logging.getLogger(__name__)

def generateImage(api_key, prompt):
    try:
        openai.api_key = api_key
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']
    except openai.error.OpenAIError as e:
        logger.error(f"Error generating image: {e}")
        return None
