# agents/memory_agent.py

import os
from tinydb import TinyDB, Query
from langchain_ollama import OllamaLLM # For Ollama LLM integration via LangChain
from langchain_core.prompts import PromptTemplate
from fastapi import HTTPException # For consistent error handling

# Initialize TinyDB for persistent memory storage
# This path is relative to where the script is executed (usually the project root via orchestrator/backend)
db = TinyDB('memory/memory_store.json')
Topic = Query()

# --- LLM Interaction Function ---
# This function now accepts an initialized LangChain OllamaLLM instance
def call_llama(llm: OllamaLLM, prompt: str) -> str:
    """
    Calls the Ollama LLM using a LangChain instance to generate a response.
    """
    try:
        # LangChain's invoke method handles the API call and response parsing
        response = llm.invoke(prompt)
        return response.strip()
    except Exception as e:
        # Catch any exceptions during LLM invocation and re-raise as HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Memory Agent: Error calling LLM: {e}"
        )

# --- Memory Management Functions ---
def get_topic_history(topic: str):
    """
    Retrieves the conversation history for a given topic from TinyDB.
    """
    result = db.search(Topic.name == topic)
    # Return a copy to prevent direct modification of the TinyDB internal list
    return result[0]["messages"].copy() if result else []

def update_memory(topic: str, user_msg: str, ai_msg: str):
    """
    Updates the conversation history for a topic in TinyDB.
    Creates a new topic entry if it doesn't exist.
    """
    new_message = {"user": user_msg, "ai": ai_msg}
    if db.contains(Topic.name == topic):
        # Atomically update the messages list
        db.update(lambda t: t["messages"].append(new_message), Topic.name == topic)
    else:
        # Insert a new topic with the first message
        db.insert({"name": topic, "messages": [new_message]})

def get_all_topics():
    """
    Retrieves a list of all existing topic names from TinyDB.
    """
    return [item["name"] for item in db.all()]

# --- Main Agent Logic ---
def run_agent(llm: OllamaLLM, topic: str, user_input: str) -> str:
    """
    Executes the memory agent logic: retrieves history, constructs prompt,
    calls LLM, and updates memory.
    """
    print(f"DEBUG: Memory Agent: Running for topic '{topic}' with input: '{user_input[:50]}...'")
    
    history = get_topic_history(topic)
    
    # Construct memory context for the LLM
    memory_context = "\n".join([f"User: {m['user']}\nAI: {m['ai']}" for m in history])
    
    # Define the prompt template for the LLM
    # The LLM should understand that it's continuing a conversation
    prompt_template = PromptTemplate.from_template(
        """
        You are an AI assistant designed for long-term research.
        You remember past conversations and notes for each topic.
        Your goal is to provide helpful, concise, and context-aware responses.

        Current Topic: {topic}

        Conversation History:
        {memory_context}

        User: {user_input}
        AI:
        """
    )

    # Create the full prompt using the template
    full_prompt = prompt_template.format(
        topic=topic,
        memory_context=memory_context if memory_context else "No prior conversation for this topic.",
        user_input=user_input
    )

    # Call the LLM with the constructed prompt
    ai_reply = call_llama(llm, full_prompt)
    
    # Update memory with the new interaction
    update_memory(topic, user_input, ai_reply)
    
    return ai_reply

