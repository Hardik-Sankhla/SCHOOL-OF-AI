# backend/main.py

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import handle_query, get_available_topics, TinyDB, Query # Import TinyDB and Query
import json
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Persistent Memory Agent System API",
    description="API for a memory-powered multi-agent system for knowledge continuity.",
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

# --- API Endpoints ---

@app.get("/topics/")
async def get_topics_endpoint():
    """
    Retrieves a list of all existing research topics.
    """
    print("INFO: Received request for topics list.")
    topics = get_available_topics()
    return {"topics": topics}

@app.post("/chat/")
async def chat_endpoint(
    topic: str = Form(...),
    user_input: str = Form(...),
    # --- UPDATED: Default LLM model to 'llama3:latest' ---
    llm_model: str = Form(os.getenv("DEFAULT_LLM_MODEL", "llama3:latest")) 
):
    """
    Handles a user message for a specific topic, processes it with the agent,
    and returns the AI response and updated history.
    """
    if not topic.strip() or not user_input.strip():
        raise HTTPException(status_code=400, detail="Topic and user input cannot be empty.")
    
    # Validate the LLM model name
    # --- UPDATED: Supported models list ---
    supported_models = ["qwen3:4b", "deepseek-r1:1.5b", "llama3:latest", "mistral:latest"] 
    if llm_model not in supported_models:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported LLM model: '{llm_model}'. Supported models are: {', '.join(supported_models)}"
        )

    print(f"INFO: Received chat request for topic: '{topic}' with model: '{llm_model}'")
    
    try:
        ai_response, history = handle_query(topic, user_input, llm_model)
        return {
            "ai_response": ai_response,
            "history": history
        }
    except HTTPException as e:
        raise e # Re-raise HTTPExceptions from orchestrator
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during chat processing: {str(e)}"
        )

@app.get("/history/{topic_name}/")
async def get_history_endpoint(topic_name: str):
    """
    Retrieves the full conversation history for a specific topic.
    """
    if not topic_name.strip():
        raise HTTPException(status_code=400, detail="Topic name cannot be empty.")
    
    print(f"INFO: Received request for history of topic: '{topic_name}'")
    db = TinyDB('memory/memory_store.json') # Re-initialize TinyDB to ensure fresh state
    Topic = Query()
    result = db.search(Topic.name == topic_name)
    history = result[0]["messages"].copy() if result else []
    
    return {"topic": topic_name, "history": history}

@app.get("/export/{topic_name}/")
async def export_topic_endpoint(topic_name: str):
    """
    Exports the full conversation history of a topic as JSON.
    """
    if not topic_name.strip():
        raise HTTPException(status_code=400, detail="Topic name cannot be empty.")
    
    print(f"INFO: Received request to export topic: '{topic_name}'")
    db = TinyDB('memory/memory_store.json') # Re-initialize TinyDB
    Topic = Query()
    result = db.search(Topic.name == topic_name)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found.")
    
    return result[0] # Return the entire topic object for export

# Ensure the memory directory exists
os.makedirs("memory", exist_ok=True)

# Example of how to run this backend:
# Make sure you have uvicorn installed: pip install uvicorn
# Run from the 'memory-agent-system' directory:
# uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
