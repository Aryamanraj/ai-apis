import logging
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Ensure the logs directory and files exist
os.makedirs("./logs", exist_ok=True)
if not os.path.exists("./logs/combined.log"):
    open("./logs/combined.log", 'w').close()
if not os.path.exists("./logs/error.log"):
    open("./logs/error.log", 'w').close()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("./logs/combined.log"),
        logging.StreamHandler()
    ]
)

# Set up error logging
error_handler = logging.FileHandler("./logs/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add error handler to root logger
root_logger = logging.getLogger()
root_logger.addHandler(error_handler)

logger = logging.getLogger(__name__)
logger.addHandler(error_handler)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
