# agents/summarize_agent.py

import os
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama # Using OllamaLLM for direct text generation
from fastapi import HTTPException

# Note: OLLAMA_API_BASE_URL, LLM_MODEL, and OLLAMA_REQUEST_TIMEOUT_SECONDS
# are now handled by the 'llm' instance passed from the orchestrator.
# This agent simply uses the provided LangChain LLM instance.

def summarize_text(llm: Ollama, text: str) -> str:
    """
    Summarizes the provided text using the given LangChain Ollama LLM instance.
    
    Args:
        llm (Ollama): An initialized LangChain Ollama LLM instance.
        text (str): The text content to be summarized.

    Returns:
        str: The summarized text.

    Raises:
        HTTPException: If an error occurs during LLM invocation.
    """
    print(f"DEBUG: Summarize Agent: Summarizing text (first 100 chars): {text[:100]}...")
    
    prompt_template = PromptTemplate.from_template(
        """
        Summarize the following research findings concisely in 3 to 5 bullet points.
        Focus on the most important aspects related to the research topic.

        Findings:
        ---
        {text}
        ---

        Summary:
        """
    )
    
    # Create a simple chain: prompt -> llm
    chain = prompt_template | llm

    try:
        # Invoke the chain with the input text
        summary = chain.invoke({"text": text})
        return summary.strip()
    except Exception as e:
        # Catch any exceptions during LLM invocation and re-raise as HTTPException
        # The specific error details (connection, timeout, JSONDecode) are handled
        # by the LangChain Ollama class internally and surfaced as a general exception.
        raise HTTPException(
            status_code=500,
            detail=f"Summarize Agent: An error occurred during LLM summarization: {e}"
        )

