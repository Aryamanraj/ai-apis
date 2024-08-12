import os
from fastapi import FastAPI
from fastapi.security import HTTPBearer

# Create a security instance
security_scheme = HTTPBearer()

app = FastAPI()

# Add middlewares
app.middleware("http")(jwt_middleware)
app.add_middleware(LoggingMiddleware)

# Add CORS
add_cors_middleware(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
