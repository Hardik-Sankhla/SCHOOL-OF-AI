# frontend.py

import streamlit as st
import requests
import json
import pandas as pd # For potential future structured data display

# --- Configuration ---
BACKEND_API_URL = "http://localhost:8000/research/" # FastAPI backend API endpoint
APP_TITLE = "🧠 Your Personal Multi-Agent Research Assistant"
# Set a generous timeout for frontend to backend requests (e.g., 9 minutes)
# This should be greater than the backend's internal LLM timeout (480s)
REQUEST_TIMEOUT_SECONDS = 5000

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖", # Changed icon for multi-agent theme
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a professional and modern look ---
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6; /* Light grey background */
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    h1 {
        color: #4a4a4a; /* Dark grey for headings */
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    h2, h3 {
        color: #333333; /* Slightly lighter dark grey */
        border-bottom: 2px solid #6c5ce7; /* Purple underline for tech theme */
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput label, .stSelectbox label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .stButton > button {
        background-color: #6c5ce7; /* Purple button */
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #5a4ac9; /* Darker purple on hover */
        transform: translateY(-2px);
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }
    .stSpinner > div > div {
        color: #6c5ce7; /* Spinner color */
    }
    .stAlert {
        border-radius: 8px;
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .stDownloadButton > button {
        background-color: #28a745; /* Green button for download */
    }
    .stDownloadButton > button:hover {
        background-color: #218838;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.title(APP_TITLE)
st.markdown(
    "<h3 style='text-align: center; color: #555;'>Leverage multiple AI agents to perform rapid research, summarize findings, and generate reports.</h3>",
    unsafe_allow_html=True
)

# --- Main Application Logic ---

# Initialize session state for topic input and results
if 'research_topic_input' not in st.session_state:
    st.session_state.research_topic_input = ""
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'selected_llm_model' not in st.session_state:
    # --- UPDATED: Set default LLM model to qwen3:4b ---
    st.session_state.selected_llm_model = "qwen3:4b" 

# Define a function to clear the input and results
def clear_all_researcher():
    if 'research_topic_input' in st.session_state:
        del st.session_state.research_topic_input
    if 'research_results' in st.session_state:
        del st.session_state.research_results
    # Note: We don't clear selected_llm_model as it's a user preference for the session
    st.rerun() # Explicitly force a rerun after clearing state

# Text input for research topic
st.subheader("💡 Enter Your Research Topic")
topic = st.text_input(
    "What topic do you want the AI agents to research?",
    placeholder="e.g., 'Latest advancements in quantum computing for drug discovery'",
    key="research_topic_input",
    value=st.session_state.research_topic_input # Ensure the text input reflects the session state
)

# LLM Model Selection
st.subheader("🤖 Choose Your LLM Model")
# --- UPDATED: Include qwen3:4b in options and ensure it's the default selection ---
llm_model_options = ["qwen3:4b", "llama2", "mistral", "gemma", "phi3"] 
selected_llm_model = st.selectbox(
    "Select the Ollama LLM model to use for the agents:",
    options=llm_model_options,
    index=llm_model_options.index(st.session_state.selected_llm_model) if st.session_state.selected_llm_model in llm_model_options else 0,
    key="llm_model_selector",
    on_change=lambda: st.session_state.update(selected_llm_model=st.session_state.llm_model_selector)
)


col1, col2 = st.columns([1, 1])

with col1:
    run_button = st.button("🚀 Run Research Pipeline")
with col2:
    clear_button = st.button("🧹 Clear All", on_click=clear_all_researcher)

# Handle Run Research button
if run_button and topic:
    with st.spinner(f"Agents are working using {selected_llm_model}... This may take a few moments."):
        try:
            # Make a POST request to the FastAPI backend, including the selected LLM model
            response = requests.post(
                BACKEND_API_URL, 
                data={"topic": topic, "llm_model": selected_llm_model}, # Pass model name
                timeout=REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            st.session_state.research_results = response.json()
            
            if st.session_state.research_results.get("error"):
                st.error(f"An error occurred during research: {st.session_state.research_results['error']['detail']}")
            else:
                st.success("Research pipeline complete!")

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the backend server. "
                "Please ensure the FastAPI backend is running at `http://localhost:8000`."
            )
            st.session_state.research_results = None
        except requests.exceptions.Timeout:
            st.error(
                f"The research request timed out after {REQUEST_TIMEOUT_SECONDS} seconds. "
                "The backend or LLM might be taking too long to respond. Consider a smaller model or more powerful hardware."
            )
            st.session_state.research_results = None
        except requests.exceptions.HTTPError as e:
            error_detail = e.response.json().get('detail', str(e))
            st.error(f"Backend error: {error_detail}")
            st.session_state.research_results = None
        except Exception as e:
            st.error(f"An unexpected error occurred while running the pipeline: {e}")
            st.session_state.research_results = None
elif run_button and not topic:
    st.warning("Please enter a research topic before running the pipeline.")

# --- Display Results ---
if st.session_state.research_results and not st.session_state.research_results.get("error"):
    results = st.session_state.research_results

    st.markdown("---") # Separator
    st.header("📊 Research Results")

    # Search Results
    st.subheader("🔍 Search Results (Simulated)")
    st.code(results.get("search", "No search results available."), language='text')

    # Summary
    st.subheader("📝 Summarized Findings")
    st.info(results.get("summary", "No summary generated."))

    # Fact Checker Feedback
    st.subheader("✅ Fact-Checker Feedback")
    st.warning(results.get("corrections", "No feedback from fact-checker."))

    # Final Report
    st.subheader("📄 Final Research Brief")
    st.markdown(results.get("report", "No final report generated."))

    # --- Download Options ---
    st.markdown("---")
    st.subheader("⬇️ Download Results")

    # Create a dictionary for all results to be downloaded as JSON
    download_data = {
        "topic": topic,
        "llm_model_used": selected_llm_model, # Include model used in download
        "search_results": results.get("search", ""),
        "summary": results.get("summary", ""),
        "corrections": results.get("corrections", ""),
        "final_report": results.get("report", "")
    }
    json_output = json.dumps(download_data, indent=4)

    st.download_button(
        label="Download All Research Results (JSON)",
        data=json_output,
        file_name="multi_agent_research_results.json",
        mime="application/json",
        help="Download all generated research outputs as a JSON file."
    )

# --- Sidebar Information ---
with st.sidebar:
    st.header("About This Tool")
    st.info(
        "This Multi-Agent Research Assistant simulates a competitive intelligence workflow "
        "by coordinating specialized AI agents to search, summarize, fact-check, and report on a given topic. "
        "It's designed for rapid information gathering and analysis."
    )
    st.header("How It Works")
    st.markdown(
        """
        1.  **Enter Topic & Select LLM:** Provide a research topic and choose your preferred local LLM model (e.g., Llama2, Mistral).
        2.  **Backend Orchestration:** The request goes to a FastAPI backend which initializes the selected LLM via LangChain and coordinates the agents.
        3.  **Search Agent:** Simulates web search to gather initial findings.
        4.  **Summarizer Agent:** Condenses the findings into a concise summary using the chosen LLM.
        5.  **Fact-Checker Agent:** Reviews the summary for potential biases or inaccuracies using the chosen LLM.
        6.  **Report Generator Agent:** Compiles a final, polished research brief incorporating all findings and feedback using the chosen LLM.
        """
    )
    st.header("Setup Instructions")
    st.markdown(
        """
        To run this application locally, follow these steps:
        1.  **Install Ollama:** Download and install Ollama from [ollama.ai](https://ollama.ai/).
        2.  **Pull Models:** Run `ollama pull llama2`, `ollama pull mistral`, and `ollama pull qwen:4b` (or any other models you want to use) in your terminal.
        3.  **Run Ollama Server:** `ollama serve` in one terminal. Keep this running. (Note: `ollama run` is for interactive chat, `ollama serve` is for API access).
        4.  **Clone Repo:** `git clone https://github.com/yourusername/multi-agent-researcher.git`
        5.  **Navigate:** `cd multi-agent-researcher`
        6.  **Install Dependencies:** `pip install -r requirements.txt`
        7.  **Start Backend:** `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000` in a new terminal.
        8.  **Run Frontend:** `streamlit run frontend/frontend.py` in another new terminal.
        """
    )
    st.markdown("---")
    st.caption("Developed for Your Personal Use | Powered by FastAPI, Streamlit, LangChain, and Ollama.")

