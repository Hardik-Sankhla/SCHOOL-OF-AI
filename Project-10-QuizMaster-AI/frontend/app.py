# frontend/app.py

import streamlit as st
import requests
import json
import pandas as pd # For potential future structured data display

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/generate/" # Updated endpoint
APP_TITLE = "📚 LearnSphere AI Tutor & Quiz Generator"
# Set a generous timeout for frontend to backend requests (e.g., 8 minutes)
REQUEST_TIMEOUT_SECONDS = 1000 

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓", # Changed icon for education theme
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a more professional and educational look ---
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
        color: #0056b3; /* Dark blue for headings */
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    h2, h3 {
        color: #004085; /* Slightly lighter dark blue */
        border-bottom: 2px solid #28a745; /* Green underline for educational theme */
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
    /* Specific styles for quiz questions and concepts */
    .quiz-question {
        font-weight: bold;
        color: #34495e;
        margin-top: 15px;
    }
    .quiz-answer {
        color: #28a745; /* Green for answers */
        font-style: italic;
    }
    .key-concept {
        color: #0056b3; /* Blue for concepts */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.title(APP_TITLE)
st.markdown(
    "<h3 style='text-align: center; color: #555;'>Generate simplified explanations, quizzes, and key concepts from educational text.</h3>",
    unsafe_allow_html=True
)

# --- Main Application Logic ---

# Initialize session state for text input and results if not already present
if 'lesson_text_input' not in st.session_state:
    st.session_state.lesson_text_input = ""
if 'results' not in st.session_state:
    st.session_state.results = None

# Define a function to clear the input and results
def clear_all_learnsphere():
    if 'lesson_text_input' in st.session_state:
        del st.session_state.lesson_text_input
    if 'results' in st.session_state:
        del st.session_state.results
    st.rerun() # Explicitly force a rerun after clearing state

# Text input area
st.subheader("📝 Paste Lesson Content or Textbook Paragraph Here")
lesson_text = st.text_area(
    "Enter the educational text you want to analyze:",
    height=400,
    placeholder="Paste lecture notes, textbook chapters, or any educational content here...",
    key="lesson_text_input",
    value=st.session_state.lesson_text_input # Ensure the text area reflects the session state
)

col1, col2 = st.columns([1, 1])

with col1:
    generate_button = st.button("🚀 Generate Learning Aids")
with col2:
    clear_button = st.button("🧹 Clear All", on_click=clear_all_learnsphere)

# Handle Generate button
if generate_button and lesson_text:
    with st.spinner("Generating learning aids... This may take a moment."):
        try:
            # Make a POST request to the FastAPI backend with an explicit timeout
            response = requests.post(BACKEND_URL, data={"text": lesson_text}, timeout=REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            st.session_state.results = response.json()
            st.success("Generation complete!")
        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the backend server. "
                "Please ensure the FastAPI backend is running at `http://localhost:8000`."
            )
            st.session_state.results = None
        except requests.exceptions.Timeout:
            st.error(
                f"The generation request timed out after {REQUEST_TIMEOUT_SECONDS} seconds. "
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
elif generate_button and not lesson_text:
    st.warning("Please paste some educational text into the input area before generating learning aids.")

# --- Display Results ---
if st.session_state.results:
    results = st.session_state.results

    st.markdown("---") # Separator
    st.header("🎓 Generated Learning Aids")

    # Simplified Explanation
    st.subheader("🧠 Simplified Explanation")
    st.info(results.get("explanation", "No simplified explanation generated."))

    # Quiz Questions & Answers
    st.subheader("📝 Quiz Questions & Answers")
    quiz_text = results.get("quiz", "No quiz questions generated.")
    # Attempt to format quiz for better readability if possible
    formatted_quiz = []
    for line in quiz_text.split('\n'):
        line = line.strip()
        if line.startswith(("1.", "2.", "3.", "4.", "5.")): # Assuming 5 questions
            formatted_quiz.append(f'<p class="quiz-question">{line}</p>')
        elif line.startswith(("A)", "B)", "C)", "D)")):
            formatted_quiz.append(f'<p>{line}</p>')
        elif line.startswith("Answer:"):
            formatted_quiz.append(f'<p class="quiz-answer">{line}</p>')
        else:
            formatted_quiz.append(f'<p>{line}</p>') # Fallback for other lines
    st.markdown("".join(formatted_quiz), unsafe_allow_html=True)
    if not quiz_text:
        st.write("No quiz questions generated.")


    # Key Concepts
    st.subheader("🔑 Key Concepts")
    concepts_text = results.get("concepts", "No key concepts found.")
    # Display concepts as markdown (assuming LLM outputs bullet points)
    st.markdown(concepts_text)
    if not concepts_text:
        st.write("No key concepts found.")

    # --- Download Options ---
    st.markdown("---")
    st.subheader("⬇️ Download Results")

    # Create a dictionary for all results to be downloaded as JSON
    download_data = {
        "explanation": results.get("explanation", ""),
        "quiz": results.get("quiz", ""),
        "concepts": results.get("concepts", "")
    }
    json_output = json.dumps(download_data, indent=4)

    st.download_button(
        label="Download All Learning Aids (JSON)",
        data=json_output,
        file_name="learnsphere_aids.json",
        mime="application/json",
        help="Download the explanation, quiz, and concepts as a JSON file."
    )

    st.download_button(
        label="Download Explanation (TXT)",
        data=results.get("explanation", ""),
        file_name="learnsphere_explanation.txt",
        mime="text/plain",
        help="Download only the simplified explanation."
    )
    st.download_button(
        label="Download Quiz (TXT)",
        data=results.get("quiz", ""),
        file_name="learnsphere_quiz.txt",
        mime="text/plain",
        help="Download only the generated quiz."
    )
    st.download_button(
        label="Download Key Concepts (TXT)",
        data=results.get("concepts", ""),
        file_name="learnsphere_concepts.txt",
        mime="text/plain",
        help="Download only the list of key concepts."
    )

# --- Sidebar Information ---
with st.sidebar:
    st.header("About This Tool")
    st.info(
        "This AI Tutor & Quiz Generator helps instructors and students at LearnSphere Academy "
        "by transforming educational content into simplified explanations, interactive quizzes, "
        "and concise lists of key concepts for better comprehension and revision."
    )
    st.header("How It Works")
    st.markdown(
        """
        1.  **Paste Content:** Enter your lecture notes or textbook content into the text area.
        2.  **Generate:** Click the "Generate Learning Aids" button.
        3.  **LLM Processing:** The text is sent to a FastAPI backend, which uses Ollama to interact with a local LLM (Mistral or Llama2).
        4.  **Results:** The LLM generates the simplified explanation, quiz questions, and key concepts, which are then displayed.
        """
    )
    st.header("Setup Instructions")
    st.markdown(
        """
        To run this application locally, follow these steps:
        1.  **Install Ollama:** Download and install Ollama from [ollama.ai](https://ollama.ai/).
        2.  **Pull Model:** Run `ollama pull mistral` (or `ollama pull llama2`) in your terminal.
        3.  **Clone Repo:** `git clone https://github.com/yourusername/ai-tutor-learnsphere.git`
        4.  **Navigate:** `cd ai-tutor-learnsphere`
        5.  **Install Dependencies:** `pip install -r requirements.txt`
        6.  **Run Backend:** `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
        7.  **Run Frontend:** `streamlit run frontend/app.py`
        """
    )
    st.markdown("---")
    st.caption("Developed for LearnSphere Academy | Powered by FastAPI, Streamlit, and Ollama.")

