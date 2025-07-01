# agents/search_agent.py

import os
from dotenv import load_dotenv # Import load_dotenv
from fastapi import HTTPException
from serpapi import GoogleSearch # SerpApi's client library is named GoogleSearch, but supports other engines

# Load environment variables from .env file
load_dotenv()

# Get SerpApi Key from environment variables
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def run_search(topic: str) -> str:
    """
    Performs a real web search for the given topic using SerpApi's DuckDuckGo engine.
    """
    if not SERPAPI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Search Agent: SERPAPI_API_KEY not found in .env. Please get one from serpapi.com and set it up."
        )

    params = {
        "engine": "duckduckgo", # Specify DuckDuckGo search engine
        "q": topic,             # The search query
        "api_key": SERPAPI_API_KEY,
        "num": 5                # Number of results to fetch (SerpApi default is often 10, but we can limit)
    }

    try:
        print(f"DEBUG: Search Agent: Performing real DuckDuckGo search for topic: '{topic}' via SerpApi...")
        
        # Initialize SerpApi search
        search = GoogleSearch(params)
        results = search.get_dict() # Execute search and get results as a dictionary

        formatted_results = []
        if "organic_results" in results:
            for i, result in enumerate(results["organic_results"]):
                title = result.get("title", "N/A")
                link = result.get("link", "N/A")
                snippet = result.get("snippet", "N/A")
                formatted_results.append(f"Result {i+1}:\nTitle: {title}\nURL: {link}\nSnippet: {snippet}\n---")
        
        if not formatted_results:
            return f"No relevant search results found for '{topic}' from DuckDuckGo via SerpApi."
            
        return "\n".join(formatted_results)

    except Exception as e:
        # SerpApi client can raise various exceptions (e.g., API errors, network issues)
        raise HTTPException(
            status_code=500,
            detail=f"Search Agent: An error occurred during SerpApi DuckDuckGo search: {e}. "
                   "Check your API key, internet connection, or SerpApi dashboard for issues."
        )

