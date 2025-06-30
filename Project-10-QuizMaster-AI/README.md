# 📚 LearnSphere AI Tutor & Quiz Generator

An intelligent AI assistant designed for LearnSphere Academy to enhance online learning by transforming educational content into simplified explanations, generating quizzes, and extracting key concepts. This tool supports both instructors in material creation and students in comprehension and retention.

## ✨ Features

- **Content Simplification:** Takes complex lecture notes or textbook content and generates a simplified, student-friendly explanation.
- **Quiz Generation:** Creates a 5-question quiz (either multiple-choice or short answer) with solutions, based on the provided educational text.
- **Key Concept Extraction:** Identifies and lists 5-10 essential terms or concepts from the learning material for quick revision.
- **User-Friendly Interface:** Intuitive web application built with Streamlit for easy content input and result viewing.
- **Robust Backend:** Powered by FastAPI for efficient handling of LLM requests and API services.
- **Local LLM Integration:** Utilizes Ollama to run open-source LLMs (e.g., Mistral, Llama2) locally, ensuring data privacy and reducing reliance on external API costs.
- **Downloadable Learning Aids:** Provides options to download the generated explanation, quiz, and concepts in JSON or plain text formats.

## 🚀 Getting Started

Follow these steps to set up and run the LearnSphere AI Tutor on your local machine.

### Prerequisites

1. **Ollama:**
    - Download and install Ollama from the official website: [ollama.ai](https://ollama.ai/).
    - Once installed, open your terminal and pull the desired LLM model. We recommend `mistral` or `llama2`:
      ```bash
      ollama pull mistral
      # or
      ollama pull llama2
      ```
    - Ensure Ollama is running in the background (it often runs as a service after installation).

2. **Python 3.8+:**
    - Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. **Create Project Directory:**
    ```bash
    mkdir ai-tutor-learnsphere
    cd ai-tutor-learnsphere
    ```
2. **Create Subdirectories:**
    ```bash
    mkdir backend frontend data
    ```
3. **Create Files:**
    - Create `data/sample_lesson.txt` and paste the sample lesson content.
    - Create `backend/main.py` and paste the backend code.
    - Create `frontend/app.py` and paste the frontend code.
    - Create `requirements.txt` and paste the dependencies list.
    - Create `README.md` and paste this content.

4. **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

5. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Ensure Ollama is running and the chosen LLM model (`mistral` or `llama2`) is pulled.

1. **Run the Backend (FastAPI):**  
    Open a new terminal window (and activate your virtual environment if you created one) in the `ai-tutor-learnsphere` directory and run:
    ```bash
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```
    This will start the FastAPI server, typically accessible at `http://localhost:8000`. The `--reload` flag will automatically restart the server on code changes.

2. **Run the Frontend (Streamlit):**  
    Open another new terminal window (and activate your virtual environment) in the `ai-tutor-learnsphere` directory and run:
    ```bash
    streamlit run frontend/app.py
    ```
    This will open the Streamlit application in your default web browser, typically at `http://localhost:8501`.

### Usage

1. **Paste Content:** In the Streamlit application, paste your educational text into the provided text area. You can use the `data/sample_lesson.txt` file for testing.
2. **Generate:** Click the "🚀 Generate Learning Aids" button. A loading spinner will appear while the LLM processes the text.
3. **View Results:** Once the generation is complete, the simplified explanation, quiz questions with answers, and key concepts will be displayed in dedicated sections.
4. **Download:** Use the "Download All Learning Aids (JSON)" or individual text download buttons to save the generated content.
5. **Clear:** Click "🧹 Clear All" to reset the input and results.

## 📁 Project Structure

```
ai-tutor-learnsphere/
├── backend/
│   └── main.py           # FastAPI backend for LLM integration and API endpoints
├── frontend/
│   └── app.py            # Streamlit frontend for the user interface
├── data/
│   └── sample_lesson.txt # Sample educational text for testing
├── requirements.txt      # List of Python dependencies
└── README.md             # Project documentation (this file)
```

## 🛠️ Technologies Used

- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
  - [Requests](https://requests.readthedocs.io/en/latest/): HTTP library for making requests to the Ollama API.
- **Frontend:**
  - [Streamlit](https://streamlit.io/): An open-source app framework for Machine Learning and Data Science teams.
  - [Pandas](https://pandas.pydata.org/): Included for general compatibility, though not directly used for structured display in this specific project.
- **Large Language Model (LLM):**
  - [Ollama](https://ollama.ai/): A platform for running open-source LLMs locally.
  - [Mistral](https://ollama.ai/library/mistral) / [Llama2](https://ollama.ai/library/llama2): Efficient open-source LLM models suitable for text generation tasks.

## ⚠️ Troubleshooting

- **"Could not connect to Ollama server":**
  - Ensure Ollama is installed and running in your system tray or as a background process.
  - Verify that you have pulled the `mistral` (or `llama2`) model using `ollama pull mistral`.
  - Check if the Ollama server is running on `http://localhost:11434`. You can change the `OLLAMA_API_BASE_URL` environment variable in `backend/main.py` if your Ollama server is on a different address/port.
- **"Backend error: Could not connect to the backend server":**
  - Ensure the FastAPI backend is running in a separate terminal window.
  - Verify that it's running on `http://localhost:8000`.
- **LLM response issues (e.g., "Unexpected response format", poor quality output):**
  - The LLM might be struggling to adhere to the prompt. Try refining the prompts in `backend/main.py` or ensuring the chosen model is fully downloaded and functional.
  - Check Ollama's logs for any errors related to model loading or generation.
- **Dependencies not found:**
  - Make sure you have activated your Python virtual environment (`source venv/bin/activate` or `.\venv\Scripts\activate`) before running `pip install -r requirements.txt`.
- **"504 Gateway Timeout":**
  - This indicates the LLM is taking too long to respond. The timeouts in both `backend/main.py` and `frontend/app.py` have been set to 480 seconds (8 minutes). If you still experience timeouts, consider:
     - Using a smaller LLM model (e.g., a quantized version of Mistral, or a model like `tinyllama`).
     - Ensuring your system has sufficient RAM and a dedicated GPU if possible, as LLM inference can be very resource-intensive.
- **`AttributeError: module 'streamlit' has no attribute 'experimental_rerun'`:**
  - This means your Streamlit version is newer. The code provided uses `st.rerun()` which is the current correct method. Ensure your `frontend/app.py` is fully updated.

## 🤝 Contributing

Feel free to fork this repository, open issues, and submit pull requests.

## 📄 License

This project is open-source and available under the MIT License.

---

*Developed with ❤️ for LearnSphere Academy*
