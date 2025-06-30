# backend/main.py

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="LexPro Legal Document Analyzer API",
    description="API for extracting summaries, key clauses, and named entities from legal documents using Ollama.",
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
LLM_MODEL = os.getenv("LLM_MODEL", "llama3") # Default to llama3, as per your Ollama logs

# --- IMPORTANT FIX: Increase timeout for Ollama call to 480 seconds (8 minutes) ---
OLLAMA_REQUEST_TIMEOUT_SECONDS = 1000

def call_llm(prompt: str) -> str:
    """
    Calls the Ollama LLM API to generate a response based on the given prompt.
    Handles potential connection errors.
    """
    try:
        response = requests.post(
            f"{OLLAMA_API_BASE_URL}/api/generate",
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS # Use the increased timeout
        )
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Ollama's /api/generate endpoint returns a JSON object with a 'response' key
        # If the response structure is different, this might need adjustment.
        response_data = response.json()
        if "response" in response_data:
            return response_data["response"].strip()
        else:
            raise ValueError(f"Unexpected response format from Ollama: {response_data}")

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
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while calling the Ollama LLM: {e}"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to decode JSON response from Ollama. Check Ollama server logs."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/analyze/")
def analyze_legal(text: str = Form(...)):
    """
    Analyzes the provided legal text to extract a summary, key clauses, and named entities.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Legal text cannot be empty.")

    # Define prompts for different extraction tasks
    # Using clear instructions and delimiters for better LLM performance
    prompts = {
        "summary": (
            "Summarize the following legal document concisely, highlighting the main purpose, "
            "parties involved, and key agreements. Focus on brevity and clarity. "
            "Document:\n\n---\n{text}\n---"
        ),
        "clauses": (
            "Extract the following key clauses from the legal text (e.g., Termination, Liability, Jurisdiction, Confidentiality), "
            "providing the full text of each clause if present. If a clause is not found, state 'Not found'. "
            "Present each clause clearly labeled. "
            "Document:\n\n---\n{text}\n---"
        ),
        "entities": (
            "Extract all named entities (e.g., parties, locations, dates, titles) from the legal document. "
            "Categorize them into 'Parties', 'Dates', 'Locations', and 'Titles'. "
            "Present the output as a list for each category. "
            "Document:\n\n---\n{text}\n---"
        )
    }

    results = {}
    for key, prompt_template in prompts.items():
        try:
            # Format the prompt with the actual legal text
            formatted_prompt = prompt_template.format(text=text)
            results[key] = call_llm(formatted_prompt)
        except HTTPException as e:
            # Re-raise HTTPException for specific error messages from call_llm
            raise e
        except Exception as e:
            # Catch any other unexpected errors during LLM call
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred during {key} extraction: {e}")

    return results

# Example of how to run this backend:
# Make sure you have uvicorn installed: pip install uvicorn
# Run from the 'legal-analyzer-lexpro' directory:
# uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
