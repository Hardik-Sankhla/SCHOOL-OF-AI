# agents/checker_agent.py

import os
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama # Using OllamaLLM for direct text generation
from fastapi import HTTPException

# Note: LLM_MODEL and OLLAMA_API_BASE_URL are now handled by the orchestrator
# and passed as an LLM instance.

def fact_check(llm: Ollama, text: str) -> str:
    """
    Checks the provided text (summary) for potential bias, hallucination, or inaccuracies
    using the given LangChain Ollama LLM instance and suggests improvements.
    """
    print(f"DEBUG: Fact-Checker Agent: Checking text (first 100 chars): {text[:100]}...")
    
    prompt_template = PromptTemplate.from_template(
        """
        Review the following summary for potential biases, factual inaccuracies, or hallucinations.
        Provide constructive feedback or suggested corrections in a concise, bulleted list.
        If the summary seems accurate and unbiased, state "No significant issues found."

        Summary to check:
        ---
        {text}
        ---

        Feedback/Corrections:
        """
    )

    chain = prompt_template | llm # Create a simple chain: prompt -> llm

    try:
        # Invoke the chain with the input text
        corrections = chain.invoke({"text": text})
        return corrections.strip()
    except Exception as e:
        # Catch any exceptions during LLM invocation and re-raise as HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Fact-Checker Agent: An error occurred during LLM fact-checking: {e}"
        )

