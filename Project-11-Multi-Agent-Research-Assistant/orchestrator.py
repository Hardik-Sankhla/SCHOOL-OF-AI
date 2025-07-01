# orchestrator.py

from agents.search_agent import run_search
from agents.summarize_agent import summarize_text
from agents.checker_agent import fact_check
from agents.report_agent import generate_report
from fastapi import HTTPException
from langchain_ollama import OllamaLLM # Updated import as per deprecation warning
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set a generous timeout for Ollama call (e.g., 8 minutes, now 2000 seconds)
OLLAMA_REQUEST_TIMEOUT_SECONDS = 10000 # Updated timeout as per your request

def run_research_pipeline(topic: str, llm_model_name: str):
    """
    Orchestrates the multi-agent research pipeline using a dynamically selected LLM.
    
    Args:
        topic (str): The research topic.
        llm_model_name (str): The name of the Ollama model to use (e.g., 'llama2', 'mistral').

    Returns:
        dict: A dictionary containing the results from each agent.
    """
    results = {
        "search": "N/A",
        "summary": "N/A",
        "corrections": "N/A",
        "report": "N/A",
        "error": None
    }

    try:
        # Initialize the LangChain Ollama LLM instance once
        # This LLM instance will be passed to all agents that need to interact with Ollama
        llm = OllamaLLM( # Changed to OllamaLLM
            model=llm_model_name,
            base_url=os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434"), # Use .env var
            temperature=0.0, # Keep temperature low for factual tasks
            num_ctx=4096, # Set context window if needed, adjust based on model capability
            # request_timeout parameter is now part of the OllamaLLM constructor
            request_timeout=OLLAMA_REQUEST_TIMEOUT_SECONDS, # Passed the timeout here
            stop=["--- End Search Results ---", "Summary:", "Feedback/Corrections:", "Final Research Brief:"] # Common stop sequences
        )
        
        # Test if Ollama is reachable and the model is loaded
        try:
            llm.invoke("Hello") # Simple test call
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Ollama connectivity issue: Could not reach Ollama server or model '{llm_model_name}' is not loaded. Error: {e}"
            )

        # Step 1: Search Agent (does not use LLM directly)
        print("Orchestrator: Running Search Agent...")
        search_results = run_search(topic)
        results["search"] = search_results

        # Step 2: Summarizer Agent
        print("Orchestrator: Running Summarizer Agent...")
        summary = summarize_text(llm, search_results) # Pass the LLM instance
        results["summary"] = summary

        # Step 3: Fact-Checker Agent
        print("Orchestrator: Running Fact-Checker Agent...")
        corrections = fact_check(llm, summary) # Pass the LLM instance
        results["corrections"] = corrections

        # Step 4: Report Generator Agent
        print("Orchestrator: Running Report Generator Agent...")
        report = generate_report(llm, summary, corrections) # Pass the LLM instance
        results["report"] = report

    except HTTPException as e:
        results["error"] = {"status_code": e.status_code, "detail": e.detail}
        print(f"Orchestrator Error (HTTPException): {e.detail}")
    except Exception as e:
        results["error"] = {"status_code": 500, "detail": f"An unexpected error occurred in orchestrator: {str(e)}"}
        print(f"Orchestrator Error (General): {e}")

    return results

