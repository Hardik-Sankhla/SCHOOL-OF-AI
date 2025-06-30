# backend/main.py

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="LearnSphere AI Tutor API",
    description="API for generating simplified explanations, quizzes, and key concepts from educational text using Ollama.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing) to allow frontend to communicate
# Adjust origins as needed for your deployment environment
origins = [
    "http://localhost",
    "http://localhost:8501",  # Default Streamlit port
    "http://127.0.0.1:8501",
    "*" # For development, allow all origins. Restrict this in production.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama server configuration
OLLAMA_API_BASE_URL = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3:latest") # Default to mistral, can be changed via env var

# Set a generous timeout for Ollama call (e.g., 8 minutes)
OLLAMA_REQUEST_TIMEOUT_SECONDS = 1000

def call_llm(prompt: str) -> str:
    """
    Calls the Ollama LLM API to generate a response based on the given prompt.
    Handles potential connection errors and unexpected responses.
    """
    try:
        response = requests.post(
            f"{OLLAMA_API_BASE_URL}/api/generate",
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS # Use the increased timeout
        )
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        response_data = response.json()
        if "response" in response_data:
            return response_data["response"].strip()
        else:
            raise ValueError(f"Unexpected response format from Ollama: 'response' key missing. Response: {response_data}")

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to Ollama server at {OLLAMA_API_BASE_URL}. "
                   "Please ensure Ollama is running and the model '{LLM_MODEL}' is pulled."
        )
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail=f"Ollama server timed out after {OLLAMA_REQUEST_TIMEOUT_SECONDS} seconds. "
                   "The LLM might be taking too long to respond. Consider a smaller model or more powerful hardware."
        )
    except requests.exceptions.RequestException as e:
        # Catch all other requests-related errors (e.g., DNS issues, invalid URL)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while calling the Ollama LLM API: {e}"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to decode JSON response from Ollama. Check Ollama server logs for malformed output."
        )
    except ValueError as e:
        # Catch value errors from unexpected LLM response format
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        # Catch any other unforeseen errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during LLM interaction: {e}"
        )

@app.post("/generate/")
def generate_learning_aids(text: str = Form(...)):
    """
    Generates a simplified explanation, a quiz, and key concepts from educational text.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Educational text cannot be empty.")

    # Define prompts for different generation tasks
    # Using clear instructions, specific formats, and delimiters for better LLM performance
    prompts = {
        "explanation": (
            "Explain the following educational text in simple, easy-to-understand terms for a student "
            "who is new to the topic. Focus on clarity and conciseness, avoiding overly technical jargon. "
            "Text:\n\n---\n{text}\n---"
        ),
        "quiz": (
            "Generate a 5-question quiz based on the following educational text. "
            "Each question should be either multiple-choice with 4 options (A, B, C, D) or a short answer question. "
            "Provide the correct answer for each question clearly marked. "
            "Format: \n\n1. Question?\nA) Option A\nB) Option B\nC) Option C\nD) Option D\nAnswer: [Correct Option]\n\n"
            "2. Short answer question?\nAnswer: [Short Answer]\n\n"
            "Text:\n\n---\n{text}\n---"
        ),
        "concepts": (
            "List 5 to 10 key concepts or terms from the following educational content. "
            "Present them as a clear bulleted list. "
            "Text:\n\n---\n{text}\n---"
        )
    }

    results = {}
    for key, prompt_template in prompts.items():
        try:
            formatted_prompt = prompt_template.format(text=text)
            results[key] = call_llm(formatted_prompt)
        except HTTPException as e:
            # Re-raise HTTPException for specific error messages from call_llm
            raise e
        except Exception as e:
            # Catch any other unexpected errors during LLM call
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred during {key} generation: {e}")

    return results

# Example of how to run this backend:
# Make sure you have uvicorn installed: pip install uvicorn
# Run from the 'ai-tutor-learnsphere' directory:
# uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
