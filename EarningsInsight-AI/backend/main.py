# backend/main.py

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os

# Initialize FastAPI app
app = FastAPI(
    title="FinScope AI Analyst API",
    description="API for summarizing earnings call transcripts, classifying sentiment, and extracting key financial insights using Ollama.",
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
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:4b") # Default to mistral, can be changed via env var

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

@app.post("/analyze/")
def analyze_call(text: str = Form(...)):
    """
    Analyzes the provided earnings call transcript to extract a summary,
    overall sentiment, and key financial insights.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Earnings call transcript cannot be empty.")

    # Define prompts for different analysis tasks
    # Using clear instructions, specific formats, and delimiters for better LLM performance
    prompts = {
        "summary": (
            "Summarize the following earnings call transcript concisely in one paragraph, "
            "highlighting key financial performance, strategic updates, and future outlook. "
            "Focus on the most important information for an investor. "
            "Transcript:\n\n---\n{text}\n---"
        ),
        "sentiment": (
            "Analyze the overall sentiment of the following earnings call transcript regarding the company's future outlook. "
            "Respond with only one word: 'Positive', 'Neutral', or 'Negative'. "
            "After the word, provide a brief, one-sentence justification. "
            "Transcript:\n\n---\n{text}\n---"
        ),
        "insights": (
            "Extract key financial signals and actionable insights from the following earnings call transcript. "
            "Categorize them into 'Revenue & Growth Forecasts', 'Risk Warnings & Challenges', and 'Strategic Investments'. "
            "Present each category as a bulleted list. If a category is not explicitly mentioned, state 'N/A'. "
            "Transcript:\n\n---\n{text}\n---"
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
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred during {key} extraction: {e}")

    return results

# Example of how to run this backend:
# Make sure you have uvicorn installed: pip install uvicorn
# Run from the 'earnings-call-analyzer' directory:
# uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
