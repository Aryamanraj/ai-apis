from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this to the allowed origins you want
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
