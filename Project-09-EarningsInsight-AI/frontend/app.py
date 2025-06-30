# frontend/app.py

import streamlit as st
import requests
import json
import pandas as pd # For potentially displaying structured data

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/analyze/"
APP_TITLE = "📈 FinScope AI Analyst" # Or "EarningsInsight AI"
# Set a generous timeout for frontend to backend requests (e.g., 8 minutes)
REQUEST_TIMEOUT_SECONDS = 1000

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a more professional and financial look ---
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
        color: #1a2a3a; /* Dark blue/grey for headings */
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    h2, h3 {
        color: #2c3e50; /* Slightly lighter dark blue */
        border-bottom: 2px solid #28a745; /* Green underline for financial theme */
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .stButton > button {
        background-color: #28a745; /* Green button */
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
        background-color: #218838; /* Darker green on hover */
        transform: translateY(-2px);
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }
    .stSpinner > div > div {
        color: #28a745; /* Spinner color */
    }
    .stAlert {
        border-radius: 8px;
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .stDownloadButton > button {
        background-color: #007bff; /* Blue button for download */
    }
    .stDownloadButton > button:hover {
        background-color: #0056b3;
    }
    /* Specific styles for sentiment display */
    .sentiment-positive {
        background-color: #d4edda; /* Light green */
        color: #155724; /* Dark green text */
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        border: 1px solid #c3e6cb;
    }
    .sentiment-negative {
        background-color: #f8d7da; /* Light red */
        color: #721c24; /* Dark red text */
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        border: 1px solid #f5c6cb;
    }
    .sentiment-neutral {
        background-color: #ffeeba; /* Light yellow */
        color: #856404; /* Dark yellow text */
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        border: 1px solid #ffc107;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.title(APP_TITLE)
st.markdown(
    "<h3 style='text-align: center; color: #555;'>Summarize earnings calls, classify sentiment, and extract key financial insights.</h3>",
    unsafe_allow_html=True
)

# --- Main Application Logic ---

# Initialize session state for text input and results if not already present
if 'earnings_call_text_input' not in st.session_state:
    st.session_state.earnings_call_text_input = ""
if 'results' not in st.session_state:
    st.session_state.results = None

# Define a function to clear the input and results
def clear_all_finscope():
    if 'earnings_call_text_input' in st.session_state:
        del st.session_state.earnings_call_text_input
    if 'results' in st.session_state:
        del st.session_state.results
    st.rerun() # Explicitly force a rerun after clearing state (updated from experimental_rerun)

# Text input area
st.subheader("📝 Paste Earnings Call Transcript Here")
call_text = st.text_area(
    "Enter the full transcript of your earnings call below:",
    height=400,
    placeholder="Paste your earnings call transcript here (e.g., from a quarterly report or a transcription service)...",
    key="earnings_call_text_input",
    value=st.session_state.earnings_call_text_input # Ensure the text area reflects the session state
)

col1, col2 = st.columns([1, 1])

with col1:
    analyze_button = st.button("🚀 Analyze Transcript")
with col2:
    clear_button = st.button("🧹 Clear All", on_click=clear_all_finscope)

# Handle Analyze button
if analyze_button and call_text:
    with st.spinner("Analyzing transcript... This may take a moment."):
        try:
            # Make a POST request to the FastAPI backend with an explicit timeout
            response = requests.post(BACKEND_URL, data={"text": call_text}, timeout=REQUEST_TIMEOUT_SECONDS)
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
            error_detail = e.response.json().get('detail', str(e))
            st.error(f"Backend error: {error_detail}")
            st.session_state.results = None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.session_state.results = None
elif analyze_button and not call_text:
    st.warning("Please paste an earnings call transcript into the input area before analyzing.")

# --- Display Results ---
if st.session_state.results:
    results = st.session_state.results

    st.markdown("---") # Separator
    st.header("📊 Analysis Results")

    # Summary
    st.subheader("📝 Earnings Call Summary")
    st.info(results.get("summary", "No summary found."))

    # Sentiment
    st.subheader("📊 Overall Sentiment")
    sentiment_raw = results.get("sentiment", "N/A").strip()
    sentiment_word = "N/A"
    sentiment_explanation = ""

    # Attempt to parse sentiment (e.g., "Positive: The company expects...")
    if ":" in sentiment_raw:
        parts = sentiment_raw.split(":", 1)
        sentiment_word = parts[0].strip().lower()
        sentiment_explanation = parts[1].strip()
    else:
        sentiment_word = sentiment_raw.lower() # Fallback if no colon

    if "positive" in sentiment_word:
        st.markdown(f'<div class="sentiment-positive">Sentiment: Positive 🎉<br>{sentiment_explanation}</div>', unsafe_allow_html=True)
    elif "negative" in sentiment_word:
        st.markdown(f'<div class="sentiment-negative">Sentiment: Negative 📉<br>{sentiment_explanation}</div>', unsafe_allow_html=True)
    elif "neutral" in sentiment_word:
        st.markdown(f'<div class="sentiment-neutral">Sentiment: Neutral ⚖️<br>{sentiment_explanation}</div>', unsafe_allow_html=True)
    else:
        st.write(f"Sentiment: {sentiment_raw}")

    # Key Insights
    st.subheader("💡 Key Financial Insights")
    insights_text = results.get("insights", "No key insights found.")
    
    # Display insights as markdown (assuming LLM outputs bullet points)
    st.markdown(insights_text)

    # --- Download Options ---
    st.markdown("---")
    st.subheader("⬇️ Download Results")

    # Create a dictionary for all results to be downloaded as JSON
    download_data = {
        "summary": results.get("summary", ""),
        "sentiment": results.get("sentiment", ""),
        "insights": results.get("insights", "")
    }
    json_output = json.dumps(download_data, indent=4)

    st.download_button(
        label="Download All Results (JSON)",
        data=json_output,
        file_name="earnings_call_analysis_results.json",
        mime="application/json",
        help="Download the summary, sentiment, and insights as a JSON file."
    )

    st.download_button(
        label="Download Summary (TXT)",
        data=results.get("summary", ""),
        file_name="earnings_call_summary.txt",
        mime="text/plain",
        help="Download only the earnings call summary."
    )
    st.download_button(
        label="Download Insights (TXT)",
        data=results.get("insights", ""),
        file_name="earnings_call_insights.txt",
        mime="text/plain",
        help="Download only the extracted key insights."
    )

# --- Sidebar Information ---
with st.sidebar:
    st.header("About This Tool")
    st.info(
        "This application assists financial analysts at FinScope Capital by "
        "automating the analysis of earnings call transcripts. It provides "
        "quick summaries, sentiment analysis, and extracts critical financial signals."
    )
    st.header("How It Works")
    st.markdown(
        """
        1.  **Paste Transcript:** Enter the earnings call transcript into the text area.
        2.  **Analyze:** Click the "Analyze Transcript" button.
        3.  **LLM Processing:** The text is sent to a FastAPI backend, which uses Ollama to interact with a local LLM (Mistral).
        4.  **Results:** The LLM generates the summary, classifies sentiment, and extracts insights, which are then displayed.
        """
    )
    st.header("Setup Instructions")
    st.markdown(
        """
        To run this application locally, follow these steps:
        1.  **Install Ollama:** Download and install Ollama from [ollama.ai](https://ollama.ai/).
        2.  **Pull Model:** Run `ollama pull mistral` (or your preferred model) in your terminal.
        3.  **Clone Repo:** `git clone https://github.com/yourusername/earnings-call-analyzer.git`
        4.  **Navigate:** `cd earnings-call-analyzer`
        5.  **Install Dependencies:** `pip install -r requirements.txt`
        6.  **Run Backend:** `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
        7.  **Run Frontend:** `streamlit run frontend/app.py`
        """
    )
    st.markdown("---")
    st.caption("Developed for FinScope Capital | Powered by FastAPI, Streamlit, and Ollama.")

