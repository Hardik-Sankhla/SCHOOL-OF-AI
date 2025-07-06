# frontend.py

import streamlit as st
import requests
import json
import time # For potential loading delays

# --- Configuration ---
BACKEND_API_BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{BACKEND_API_BASE_URL}/chat/"
TOPICS_ENDPOINT = f"{BACKEND_API_BASE_URL}/topics/"
HISTORY_ENDPOINT_PREFIX = f"{BACKEND_API_BASE_URL}/history/"
EXPORT_ENDPOINT_PREFIX = f"{BACKEND_API_BASE_URL}/export/"

APP_TITLE = "🧠 Persistent Memory Agent System"
REQUEST_TIMEOUT_SECONDS = 540 # Generous timeout for backend calls

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Brand-Aligned Custom CSS ---
st.markdown("""
    <style>
    /* Brand Colors: #ffffff, #161616, #282854, #3b3a92, #4e4cd0 */

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff; /* Main background color */
        color: #161616; /* Default text color */
    }
    .main .block-container {
        padding: 2rem 5rem; /* Consistent padding for main content */
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
    h1 {
        color: #3b3a92; /* Brand color for main title */
        text-align: center;
        margin-bottom: 1.5rem;
    }
    h2, h3 {
        color: #282854; /* Dark blue-purple for subheadings */
        border-bottom: 2px solid #4e4cd0; /* Vibrant blue-purple underline */
        padding-bottom: 0.4rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stTextInput > label, .stSelectbox > label, .stTextArea > label {
        color: #282854; /* Dark blue-purple for input labels */
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton > button {
        background-color: #3b3a92; /* Medium blue-purple button */
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.2s ease-in-out;
        width: 100%; /* Ensure buttons fill their column */
    }
    .stButton > button:hover {
        background-color: #4e4cd0; /* Vibrant blue-purple on hover */
        transform: translateY(-1px);
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    .stDownloadButton > button {
        background-color: #28a745; /* Keeping green for download button for clarity */
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.2s ease-in-out;
    }
    .stDownloadButton > button:hover {
        background-color: #218838; /* Darker green on hover */
    }
    .stSpinner > div > div {
        color: #4e4cd0; /* Vibrant blue-purple for spinner */
    }
    .stAlert {
        border-radius: 8px;
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #161616; /* Very dark grey for general text */
    }
    
    /* --- Chat Bubble Colors (Lighter Tints) --- */
    .chat-bubble {
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 10px;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.05); /* Subtle shadow for depth */
    }
    .chat-bubble.user {
        background-color: rgba(78, 76, 208, 0.05); /* Very light tint of vibrant purple */
        align-self: flex-end;
        margin-left: auto;
    }
    .chat-bubble.ai {
        background-color: rgba(40, 40, 84, 0.03); /* Even lighter tint of dark blue-purple */
        align-self: flex-start;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session Initialization ---
for key, default in {
    'current_topic': None,
    'chat_history': [],
    'available_topics': [],
    'user_input_text': "",
    'selected_llm_model': "llama3:latest"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Helper Functions ---
def fetch_topics():
    try:
        response = requests.get(TOPICS_ENDPOINT, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        st.session_state.available_topics = response.json().get("topics", [])
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to backend. Ensure FastAPI server is running at http://localhost:8000.")
        st.session_state.available_topics = []
    except Exception as e:
        st.error(f"An error occurred while fetching topics: {e}")
        st.session_state.available_topics = []

def fetch_history(topic_name):
    try:
        response = requests.get(f"{HISTORY_ENDPOINT_PREFIX}{topic_name}/", timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        st.session_state.chat_history = response.json().get("history", [])
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.warning(f"No history found for topic '{topic_name}'. Starting a fresh conversation.")
            st.session_state.chat_history = []
        else:
            st.error(f"Could not fetch topic history. Backend error: {e.response.json().get('detail', str(e))}")
            st.session_state.chat_history = []
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend to fetch history. Ensure FastAPI server is running.")
        st.session_state.chat_history = []
    except Exception as e:
        st.error(f"An unexpected error occurred while fetching history: {e}")
        st.session_state.chat_history = []

def send_message():
    if st.session_state.user_input_text and st.session_state.current_topic:
        with st.spinner("Thinking..."):
            try:
                data = {
                    "topic": st.session_state.current_topic,
                    "user_input": st.session_state.user_input_text,
                    "llm_model": st.session_state.selected_llm_model
                }
                response = requests.post(CHAT_ENDPOINT, data=data, timeout=REQUEST_TIMEOUT_SECONDS)
                response.raise_for_status()
                result = response.json()
                st.session_state.chat_history = result.get("history", [])
                st.session_state.user_input_text = "" # Clear input box after sending
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Ensure FastAPI server is running.")
            except requests.exceptions.Timeout:
                st.error(f"Request timed out after {REQUEST_TIMEOUT_SECONDS} seconds. The LLM might be taking too long to respond.")
            except requests.exceptions.HTTPError as e:
                error_detail = e.response.json().get('detail', str(e))
                st.error(f"Backend error: {error_detail}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please select a topic and enter your message.")

def on_topic_change():
    selected = st.session_state.topic_selector
    if selected == "Start new topic":
        st.session_state.current_topic = None # Clear current topic until new name is entered
        st.session_state.chat_history = []
    else:
        st.session_state.current_topic = selected
        fetch_history(selected)

def clear_session_data():
    # Reset all relevant session state variables
    st.session_state.current_topic = None
    st.session_state.chat_history = []
    st.session_state.available_topics = []
    st.session_state.user_input_text = ""
    st.session_state.selected_llm_model = "llama3:latest" # Reset to default LLM model
    st.rerun() # Force a rerun to clear the UI

# --- Main UI ---
st.title(APP_TITLE)
st.markdown(
    "<h3 style='text-align: center; color: #282854;'>Your AI assistant for research memory & ongoing context.</h3>",
    unsafe_allow_html=True
)

# --- Sidebar ---
with st.sidebar:
    st.header("Manage Topics")
    if st.button("🔄 Refresh Topics"):
        fetch_topics()

    topic_options = ["Start new topic"] + st.session_state.available_topics
    selected_topic_ui = st.selectbox(
        "Choose or create a topic:",
        options=topic_options,
        key="topic_selector",
        on_change=on_topic_change
    )

    if selected_topic_ui == "Start new topic":
        new_topic = st.text_input("Enter new topic name:", key="new_topic_input")
        if new_topic and not st.session_state.current_topic:
            st.session_state.current_topic = new_topic
            st.success(f"New topic '{new_topic}' created. Start chatting!")
            # No need to fetch history for a brand new topic, it's empty
    elif st.session_state.current_topic is None and st.session_state.available_topics:
        # This handles initial load where no topic is selected but topics exist
        st.session_state.current_topic = st.session_state.available_topics[0]
        fetch_history(st.session_state.current_topic)

    st.markdown("---")
    st.header("LLM Model")
    model_list = ["qwen3:4b", "deepseek-r1:1.5b", "llama3:latest", "mistral:latest"]
    st.selectbox(
        "Select Model:",
        options=model_list,
        index=model_list.index(st.session_state.selected_llm_model),
        key="llm_model_selector",
        on_change=lambda: st.session_state.update(selected_llm_model=st.session_state.llm_model_selector)
    )

    st.markdown("---")
    st.button("🧹 Clear Session", on_click=clear_session_data)
    st.caption("Clears UI state only. Persistent memory remains.")

# --- Chat Display ---
st.header(f"Topic: {st.session_state.current_topic or 'Not Selected'}")

# Use a container to hold chat messages, ensuring they stack correctly
chat_display_area = st.container()

with chat_display_area:
    for message in st.session_state.chat_history:
        if "user" in message:
            st.markdown(f"<div class='chat-bubble user'><b>You:</b> {message['user']}</div>", unsafe_allow_html=True)
        if "ai" in message:
            st.markdown(f"<div class='chat-bubble ai'><b>AI:</b> {message['ai']}</div>", unsafe_allow_html=True)

# --- Input Area (at the bottom) ---
user_input_col, submit_col = st.columns([4, 1])
with user_input_col:
    st.text_area(
        "Your message or research note:",
        key="user_input_text",
        height=100,
        placeholder="Type your message...",
        # Removed on_change to prevent premature submission and UI changes while typing
    )
with submit_col:
    st.markdown("<br>", unsafe_allow_html=True) # Adds vertical space to align button
    st.button("Send", on_click=send_message)

# --- Export Functionality ---
if st.session_state.current_topic:
    st.markdown("---")
    st.subheader("Export Topic Data")
    
    # Use a unique key for the export button to avoid re-rendering issues
    if st.button(f"Export '{st.session_state.current_topic}' History", key="export_button"):
        try:
            response = requests.get(f"{EXPORT_ENDPOINT_PREFIX}{st.session_state.current_topic}/", timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            export_data = response.json()
            
            # The download button needs to be rendered immediately after the action
            st.download_button(
                label=f"Download {st.session_state.current_topic}.json",
                data=json.dumps(export_data, indent=4),
                file_name=f"{st.session_state.current_topic}_memory.json",
                mime="application/json",
                key="download_json_button" # Unique key for download button
            )
            st.success("Data ready for download! Click the 'Download' button above.")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to backend to export data. Ensure FastAPI server is running.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Error exporting data: {e.response.json().get('detail', str(e))}")
        except Exception as e:
            st.error(f"An unexpected error occurred during export: {e}")

# --- Initial Topic Fetch on App Load ---
# This block ensures topics are loaded when the app first starts or is refreshed
if not st.session_state.available_topics and st.session_state.current_topic is None:
    fetch_topics()
    if st.session_state.available_topics:
        # Automatically select the first topic if available
        st.session_state.current_topic = st.session_state.available_topics[0]
        fetch_history(st.session_state.current_topic)
        # Rerun to update the UI with the selected topic and its history
        st.rerun() 
    else:
        st.info("No topics found. Start by creating a new topic on the left sidebar.")

