# agents/report_agent.py

import os
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama # Using OllamaLLM for direct text generation
from fastapi import HTTPException

# Note: LLM_MODEL and OLLAMA_API_BASE_URL are now handled by the orchestrator
# and passed as an LLM instance.

def generate_report(llm: Ollama, summary: str, corrections: str) -> str:
    """
    Generates a final research brief based on the summary and fact-checker's corrections
    using the given LangChain Ollama LLM instance.
    """
    print(f"DEBUG: Report Generator Agent: Generating report...")
    
    prompt_template = PromptTemplate.from_template(
        """
        You are a professional research report generator.
        Using the provided summary and any fact-check comments/corrections, write a concise,
        actionable research brief. Structure it with an Executive Summary, Key Findings (from summary),
        and a section for 'Considerations/Caveats' (from corrections).

        Executive Summary: (1-2 sentences)
        Key Findings: (bullet points from summary)
        Considerations/Caveats: (bullet points from corrections, if any, otherwise state 'None identified')

        Summary from Summarizer Agent:
        ---
        {summary}
        ---

        Feedback/Corrections from Fact-Checker Agent:
        ---
        {corrections}
        ---

        Final Research Brief:
        """
    )

    chain = prompt_template | llm # Create a simple chain: prompt -> llm

    try:
        # Invoke the chain with the summary and corrections
        report = chain.invoke({"summary": summary, "corrections": corrections})
        return report.strip()
    except Exception as e:
        # Catch any exceptions during LLM invocation and re-raise as HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Report Generator Agent: An error occurred during LLM report generation: {e}"
        )

