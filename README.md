
---

# FastAPI Project

This FastAPI project provides two main endpoints: one for generating a challenge based on a prompt, and another for generating an image based on a prompt.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Generate Challenge](#generate-challenge)
  - [Generate Image](#generate-image)
- [Authorization](#authorization)

## Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd ai-apis
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root directory with the following content:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    JWT_SECRET=your_jwt_secret
    JWT_ALGORITHM=HS256
    ```

2. Ensure your `.env` file is populated with your actual OpenAI API key and JWT settings.

## Running the Application

To start the FastAPI application, run:

```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

or using start.sh
```sh
bash start.sh
```

The application will be available at `http://0.0.0.0:8001`.

## API Endpoints

### Generate Challenge

- **Endpoint**: `POST /generate-challenge`
- **Description**: Generates a challenge title and description based on the provided prompt.
- **Request Body**:
    - `prompt` (text): The text prompt to generate the challenge from.
    - `Authorization` (Bearer Token): The JWT token for authorization.
- **Response Body**:

    ```json
    {
        "challenge_title": "....",
        "challenge_description": "some description ..."
    }
    ```

- **Example Request**:

    ```sh
    curl -X POST "/generate-challenge/" \
    -H "Authorization: Bearer <your-jwt-token>" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Create a new AI challenge"}'
    ```

### Generate Image

- **Endpoint**: `POST /generate-image`
- **Description**: Generates an image based on the provided prompt.
- **Request Body**:
    - `prompt` (text): The text prompt to generate the image from.
    - `Authorization` (Bearer Token): The JWT token for authorization.
- **Response Body**:

    ```json
    {
        "image_url": " "
    }
    ```

- **Example Request**:

    ```sh
    curl -X POST "http://0.0.0.0:8001/generate-image/" \
    -H "Authorization: Bearer <your-jwt-token>" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Generate an image of a futuristic city"}'
    ```

## Authorization

Both endpoints require a JWT token for authorization. The token should be included in the `Authorization` header of the request in the format `Bearer <your-jwt-token>`.

Make sure to replace `<your-jwt-token>` with an actual valid token.

---
