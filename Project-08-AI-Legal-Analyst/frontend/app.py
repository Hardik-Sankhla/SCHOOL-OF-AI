# frontend/app.py

import streamlit as st
import requests
import json
import pandas as pd # For potentially displaying entities in a table

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/analyze/"
APP_TITLE = "⚖️ LexPro Legal Document Analyzer"
REQUEST_TIMEOUT_SECONDS = 1000 # Set a generous timeout for frontend to backend requests (6 minutes)

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a more professional look ---
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
        color: #2c3e50; /* Darker blue for headings */
        text-align: center;
        margin-bottom: 1.5rem;
    }
    h2, h3 {
        color: #34495e; /* Slightly lighter dark blue */
        border-bottom: 2px solid #3498db; /* Blue underline */
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stTextArea label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .stButton > button {
        background-color: #3498db; /* Blue button */
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
        background-color: #2980b9; /* Darker blue on hover */
        transform: translateY(-2px);
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }
    .stSpinner > div > div {
        color: #3498db; /* Spinner color */
    }
    .stAlert {
        border-radius: 8px;
    }
    .stMarkdown p {
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .stDownloadButton > button {
        background-color: #27ae60; /* Green button for download */
    }
    .stDownloadButton > button:hover {
        background-color: #229954;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.title(APP_TITLE)
st.markdown(
    "<h3 style='text-align: center; color: #555;'>AI-powered tool for extracting summaries, key clauses, and named entities from legal documents.</h3>",
    unsafe_allow_html=True
)

# --- Main Application Logic ---

# Initialize session state for text input and results if not already present
# This block will now re-initialize if keys are deleted by clear_all_lexpro()
if 'legal_text_input' not in st.session_state:
    st.session_state.legal_text_input = ""
if 'results' not in st.session_state:
    st.session_state.results = None

# Define a function to clear the input and results
def clear_all_lexpro():
    if 'legal_text_input' in st.session_state:
        del st.session_state.legal_text_input # Delete the key
    if 'results' in st.session_state:
        del st.session_state.results # Delete the key
    st.experimental_rerun() # Explicitly force a rerun after clearing state

# Text input area
st.subheader("📄 Paste Your Legal Document Here")
# The value of the text area is now explicitly tied to session_state.legal_text_input
text_input = st.text_area(
    "Enter the full text of your legal document below:",
    height=400,
    placeholder="Paste your contract, case file, or court ruling here...",
    key="legal_text_input",
    value=st.session_state.legal_text_input # Ensure the text area reflects the session state
)

col1, col2 = st.columns([1, 1])

with col1:
    analyze_button = st.button("🚀 Analyze Document")
with col2:
    # Use on_click to call the clear_all_lexpro function
    clear_button = st.button("🧹 Clear All", on_click=clear_all_lexpro)

# Handle Analyze button
if analyze_button and text_input:
    with st.spinner("Analyzing document... This may take a moment."):
        try:
            # Make a POST request to the FastAPI backend with an explicit timeout
            response = requests.post(BACKEND_URL, data={"text": text_input}, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            st.session_state.results = response.json()
            st.success("Analysis complete!")
        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the backend server. "
                "Please ensure the FastAPI backend is running at `http://localhost:8000`."
            )
            st.session_state.results = None
        except requests.exceptions.Timeout:
            st.error(
                f"The analysis request timed out after {REQUEST_TIMEOUT_SECONDS} seconds. "
                "The LLM might be taking too long to respond. Consider a smaller model or more powerful hardware."
            )
            st.session_state.results = None
        except requests.exceptions.HTTPError as e:
            st.error(f"Backend error: {e.response.json().get('detail', str(e))}")
            st.session_state.results = None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.session_state.results = None
elif analyze_button and not text_input:
    st.warning("Please paste some legal text into the input area before analyzing.")

# --- Display Results ---
if st.session_state.results:
    results = st.session_state.results

    st.markdown("---") # Separator
    st.header("📊 Analysis Results")

    # Summary
    st.subheader("📄 Document Summary")
    st.info(results.get("summary", "No summary found."))

    # Key Clauses
    st.subheader("📌 Key Clauses Extracted")
    st.markdown(results.get("clauses", "No key clauses found."))

    # Named Entities
    st.subheader("🔍 Named Entities Identified")
    entities_text = results.get("entities", "No named entities found.")

    # Attempt to parse entities into a more structured format if possible
    # This is a heuristic and might need adjustment based on LLM output format
    try:
        # Simple parsing for list-like output from LLM
        if "Parties:" in entities_text or "Dates:" in entities_text or "Locations:" in entities_text or "Titles:" in entities_text:
            parsed_entities = {}
            current_category = None
            for line in entities_text.split('\n'):
                line = line.strip()
                if line.startswith("Parties:"):
                    current_category = "Parties"
                    parsed_entities[current_category] = []
                elif line.startswith("Dates:"):
                    current_category = "Dates"
                    parsed_entities[current_category] = []
                elif line.startswith("Locations:"):
                    current_category = "Locations"
                    parsed_entities[current_category] = []
                elif line.startswith("Titles:"):
                    current_category = "Titles"
                    parsed_entities[current_category] = []
                elif current_category and line and not line.startswith("-"): # Avoid markdown list items that are just hyphens
                    # Attempt to clean and add entity
                    entity = line.replace("- ", "").strip()
                    if entity:
                        parsed_entities[current_category].append(entity)
            
            if parsed_entities:
                # Convert to a DataFrame for better display
                df_entities = pd.DataFrame([
                    {"Category": cat, "Entity": ent}
                    for cat, ents in parsed_entities.items() for ent in ents
                ])
                st.dataframe(df_entities, use_container_width=True)
            else:
                st.write(entities_text) # Fallback to raw text if parsing fails
        else:
            st.write(entities_text) # Fallback to raw text if expected keywords not found
    except Exception as e:
        st.warning(f"Could not parse entities into structured format. Displaying raw text. Error: {e}")
        st.write(entities_text) # Display raw text if parsing fails

    # --- Download Options ---
    st.markdown("---")
    st.subheader("⬇️ Download Results")

    # Create a dictionary for all results to be downloaded as JSON
    download_data = {
        "summary": results.get("summary", ""),
        "clauses": results.get("clauses", ""),
        "entities": results.get("entities", "")
    }
    json_output = json.dumps(download_data, indent=4)

    st.download_button(
        label="Download All Results (JSON)",
        data=json_output,
        file_name="legal_analysis_results.json",
        mime="application/json",
        help="Download the summary, clauses, and entities as a JSON file."
    )

    # You could also add options to download individual sections as text files
    st.download_button(
        label="Download Summary (TXT)",
        data=results.get("summary", ""),
        file_name="legal_summary.txt",
        mime="text/plain",
        help="Download only the document summary."
    )
    st.download_button(
        label="Download Key Clauses (TXT)",
        data=results.get("clauses", ""),
        file_name="legal_clauses.txt",
        mime="text/plain",
        help="Download only the extracted key clauses."
    )

# --- Sidebar Information ---
with st.sidebar:
    st.header("About This Tool")
    st.info(
        "This application helps legal professionals quickly analyze documents by "
        "extracting key information using a local Large Language Model (LLM) via Ollama. "
        "It provides a concise summary, identifies important clauses, and lists named entities."
    )
    st.header("How It Works")
    st.markdown(
        """
        1.  **Paste Text:** Enter your legal document into the text area.
        2.  **Analyze:** Click the "Analyze Document" button.
        3.  **LLM Processing:** The text is sent to a FastAPI backend, which uses Ollama to interact with a local LLM (e.g., Llama2).
        4.  **Results:** The LLM generates the summary, extracts clauses, and identifies entities, which are then displayed here.
        """
    )
    st.header("Setup Instructions")
    st.markdown(
        """
        To run this application locally, follow these steps:
        1.  **Install Ollama:** Download and install Ollama from [ollama.ai](https://ollama.ai/).
        2.  **Pull Model:** Run `ollama pull llama2` (or your preferred model) in your terminal.
        3.  **Clone Repo:** `git clone https://github.com/yourusername/legal-analyzer-lexpro.git`
        4.  **Navigate:** `cd legal-analyzer-lexpro`
        5.  **Install Dependencies:** `pip install -r requirements.txt`
        6.  **Run Backend:** `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
        7.  **Run Frontend:** `streamlit run frontend/app.py`
        """
    )
    st.markdown("---")
    st.caption("Developed for LexPro Law Firm | Powered by FastAPI, Streamlit, and Ollama.")

