import os
from fastapi import FastAPI
from app.middleware.jwt_middleware import jwt_middleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.api.v1.endpoints import generate_description, generate_image
from app.core.cors import add_cors_middleware
from fastapi.security import HTTPBearer

# Create a security instance
security_scheme = HTTPBearer()

app = FastAPI()

# Add middlewares
app.middleware("http")(jwt_middleware)
app.add_middleware(LoggingMiddleware)

# Add CORS
add_cors_middleware(app)

# Include routers
app.include_router(generate_description.router, prefix="/generate-description", tags=["generate-description"])
app.include_router(generate_image.router, prefix="/generate-image", tags=["generate-image"])

chat_sessions = {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
