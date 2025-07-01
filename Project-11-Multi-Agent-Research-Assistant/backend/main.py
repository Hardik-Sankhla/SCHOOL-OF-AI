# backend/main.py (FastAPI Backend with LangChain)

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import run_research_pipeline # Import the orchestrator
import json
import os # Import os for environment variables
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent Research Assistant API",
    description="API for coordinating AI agents to perform research and generate reports using LangChain and Ollama.",
    version="1.0.0"
)

# Configure CORS to allow the Streamlit frontend to communicate with this backend
origins = [
    "http://localhost",
    "http://localhost:8501",  # Default Streamlit port
    "http://127.0.0.1:8501",
    "*" # For development, allow all origins. RESTRICT THIS IN PRODUCTION.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/research/")
async def research_endpoint(topic: str = Form(...), llm_model: str = Form(os.getenv("DEFAULT_LLM_MODEL", "llama2"))): # Use .env for default
    """
    Endpoint to trigger the multi-agent research pipeline.
    Accepts a research topic and an LLM model name, then returns the comprehensive research results.
    """
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Research topic cannot be empty.")
    
    # Validate the LLM model name
    # --- UPDATED: Added 'qwen3:4b' to supported_models list ---
    supported_models = ["llama2", "mistral", "gemma", "phi3", "qwen3:4b"] # Add/remove models you support
    if llm_model not in supported_models:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported LLM model: '{llm_model}'. Supported models are: {', '.join(supported_models)}"
        )

    print(f"INFO: Received research request for topic: '{topic}' using model: '{llm_model}'")
    
    # Call the orchestration pipeline, passing the selected LLM model name
    results = run_research_pipeline(topic, llm_model)

    if results.get("error"):
        error_info = results["error"]
        raise HTTPException(
            status_code=error_info.get("status_code", 500),
            detail=error_info.get("detail", "An unknown error occurred during research pipeline execution.")
        )
    
    return results

# Example of how to run this backend:
# Make sure you have uvicorn installed: pip install uvicorn
# Run from the 'multi-agent-researcher' directory:
# uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
