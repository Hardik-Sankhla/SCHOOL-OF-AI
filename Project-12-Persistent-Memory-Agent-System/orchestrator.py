# orchestrator.py

import os
from dotenv import load_dotenv # Import load_dotenv
from fastapi import HTTPException
from langchain_ollama import OllamaLLM # For Ollama LLM integration via LangChain
from agents.memory_agent import run_agent, get_topic_history, get_all_topics, TinyDB, Query # Import TinyDB and Query

# Load environment variables from .env file
load_dotenv()

# Set a generous timeout for Ollama call (e.g., 2000 seconds)
OLLAMA_REQUEST_TIMEOUT_SECONDS = 2000

# Initialize TinyDB for memory management (ensure this path is correct relative to execution)
# This is initialized here to be accessible for get_all_topics and handle_query
db = TinyDB('memory/memory_store.json')

def get_llm_instance(llm_model_name: str) -> OllamaLLM:
    """
    Initializes and returns a LangChain OllamaLLM instance.
    Includes a test call to ensure connectivity and model loading.
    """
    try:
        llm = OllamaLLM(
            model=llm_model_name,
            base_url=os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434"),
            temperature=0.0, # Keep temperature low for factual/consistent responses
            num_ctx=4096, # Adjust context window as needed for your LLM
            request_timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS,
            stop=["User:", "AI:"] # Common stop sequences for conversational turns
        )
        # Simple test call to ensure Ollama is reachable and the model is loaded
        llm.invoke("Hello")
        return llm
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama connectivity issue: Could not reach Ollama server or model '{llm_model_name}' is not loaded. Error: {e}"
        )

def handle_query(topic: str, user_input: str, llm_model_name: str):
    """
    Handles a user query for a specific topic, orchestrating the memory agent.
    """
    print(f"Orchestrator: Handling query for topic '{topic}' with model '{llm_model_name}'")
    
    try:
        llm = get_llm_instance(llm_model_name)
        response = run_agent(llm, topic, user_input)
        history = get_topic_history(topic) # Get updated history after agent runs
        return response, history
    except HTTPException as e:
        print(f"Orchestrator Error (HTTPException): {e.detail}")
        raise # Re-raise the HTTPException for FastAPI to catch
    except Exception as e:
        print(f"Orchestrator Error (General): {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred in orchestrator: {str(e)}"
        )

def get_available_topics():
    """
    Retrieves a list of all topics stored in memory.
    """
    print("Orchestrator: Getting available topics...")
    try:
        return get_all_topics()
    except Exception as e:
        print(f"Orchestrator Error (Get Topics): {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred retrieving topics: {str(e)}"
        )

