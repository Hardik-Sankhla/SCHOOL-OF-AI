# 📈 FinScope AI Analyst (EarningsInsight AI)

An AI-powered assistant designed for FinScope Capital to analyze earnings call transcripts. This tool automates the process of summarizing key highlights, classifying market sentiment regarding future outlook, and extracting actionable financial insights, leveraging a local Large Language Model (LLM) via Ollama.

## ✨ Features

* **Transcript Analysis:** Accepts raw earnings call transcripts (copy/paste).
* **Concise Summarization:** Generates a brief, one-paragraph summary of the call's most important points.
* **Sentiment Classification:** Determines the overall sentiment (Positive, Neutral, or Negative) of the company's future outlook based on the transcript.
* **Key Financial Insight Extraction:** Identifies and extracts crucial financial signals, categorized into Revenue & Growth Forecasts, Risk Warnings & Challenges, and Strategic Investments.
* **User-Friendly Interface:** Intuitive web application built with Streamlit for easy interaction.
* **Robust Backend:** Powered by FastAPI for efficient handling of LLM requests and API services.
* **Local LLM Integration:** Utilizes Ollama to run LLMs (e.g., Mistral) locally, ensuring data privacy and reducing external API costs.
* **Downloadable Results:** Provides options to download the analysis results in JSON or plain text formats.

## 🚀 Getting Started

Follow these steps to set up and run the FinScope AI Analyst on your local machine.

### Prerequisites

1.  **Ollama:**
    * Download and install Ollama from the official website: [ollama.ai](https://ollama.ai/).
    * Once installed, open your terminal and pull the `mistral` LLM model (or your preferred alternative):
        ```bash
        ollama pull mistral
        ```
    * Ensure Ollama is running in the background (it often runs as a service after installation).

2.  **Python 3.8+:**
    * Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1.  **Create Project Directory:**
    ```bash
    mkdir earnings-call-analyzer
    cd earnings-call-analyzer
    ```
2.  **Create Subdirectories:**
    ```bash
    mkdir backend frontend data
    ```
3.  **Create Files:**
    * Create `data/tesla_q4_2024.txt` and paste the sample transcript.
    * Create `backend/main.py` and paste the backend code.
    * Create `frontend/app.py` and paste the frontend code.
    * Create `requirements.txt` and paste the dependencies list.
    * Create `README.md` and paste this content.

4.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

5.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Ensure Ollama is running and the `mistral` model is pulled.

1.  **Run the Backend (FastAPI):**
    Open a new terminal window (and activate your virtual environment if you created one) in the `earnings-call-analyzer` directory and run:
    ```bash
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```
    This will start the FastAPI server, typically accessible at `http://localhost:8000`. The `--reload` flag will automatically restart the server on code changes.

2.  **Run the Frontend (Streamlit):**
    Open another new terminal window (and activate your virtual environment) in the `earnings-call-analyzer` directory and run:
    ```bash
    streamlit run frontend/app.py
    ```
    This will open the Streamlit application in your default web browser, typically at `http://localhost:8501`.

### Usage

1.  **Paste Transcript:** In the Streamlit application, paste the full text of your earnings call transcript into the provided text area. You can use the `data/tesla_q4_2024.txt` file for testing.
2.  **Analyze:** Click the "🚀 Analyze Transcript" button. A loading spinner will appear while the LLM processes the text.
3.  **View Results:** Once the analysis is complete, the summary, sentiment classification, and key financial insights will be displayed in dedicated sections.
4.  **Download:** Use the "Download All Results (JSON)" or individual text download buttons to save the extracted information.
5.  **Clear:** Click "🧹 Clear All" to reset the input and results.

## 📁 Project Structure


earnings-call-analyzer/
├── backend/
│   └── main.py           # FastAPI backend for LLM integration and API endpoints
├── frontend/
│   └── app.py            # Streamlit frontend for the user interface
├── data/
│   └── tesla_q4_2024.txt # Sample earnings call transcript for testing
├── requirements.txt      # List of Python dependencies
└── README.md             # Project documentation (this file)


## 🛠️ Technologies Used

* **Backend:**
    * [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
    * [Requests](https://requests.readthedocs.io/en/latest/): HTTP library for making requests to the Ollama API.
* **Frontend:**
    * [Streamlit](https://streamlit.io/): An open-source app framework for Machine Learning and Data Science teams.
    * [Pandas](https://pandas.pydata.org/): Included for potential future structured data display.
* **Large Language Model (LLM):**
    * [Ollama](https://ollama.ai/): A platform for running open-source LLMs locally.
    * [Mistral](https://ollama.ai/library/mistral): A lightweight and efficient open-source LLM model.

## ⚠️ Troubleshooting

* **"Could not connect to Ollama server"**:
    * Ensure Ollama is installed and running in your system tray or as a background process.
    * Verify that you have pulled the `mistral` model using `ollama pull mistral`.
    * Check if the Ollama server is running on `http://localhost:11434`. You can change the `OLLAMA_API_BASE_URL` environment variable in `backend/main.py` if your Ollama server is on a different address/port.
* **"Backend error: Could not connect to the backend server"**:
    * Ensure the FastAPI backend is running in a separate terminal window.
    * Verify that it's running on `http://localhost:8000`.
* **LLM response issues (e.g., "Unexpected response format")**:
    * The LLM might be struggling to adhere to the prompt. Try refining the prompts in `backend/main.py` or ensuring the `mistral` model is fully downloaded and functional.
    * Check Ollama's logs for any errors related to model loading or generation.
* **Dependencies not found**:
    * Make sure you have activated your Python virtual environment (`source venv/bin/activate` or `.\venv\Scripts\activate`) before running `pip install -r requirements.txt`.
* **"504 Gateway Timeout"**:
    * This indicates the LLM is taking too long to respond. The timeouts in both `backend/main.py` and `frontend/app.py` have been set to 480 seconds (8 minutes). If you still experience timeouts, consider:
        * Using a smaller LLM model (e.g., a quantized version of Mistral, or a model like `tinyllama`).
        * Ensuring your system has sufficient RAM and a dedicated GPU if possible, as LLM inference can be very resource-intensive.

## 🤝 Contributing

Feel free to fork this repository, open issues, and submit pull requests.

## 📄 License

This project is open-source and available under the MIT License.

---
*Developed with ❤️ for FinScope Capital*
