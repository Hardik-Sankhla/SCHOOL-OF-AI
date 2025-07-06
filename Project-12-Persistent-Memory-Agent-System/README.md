# 🧠 Persistent Memory Agent System for Knowledge Continuity

> **An AI assistant that remembers conversations and research topics across sessions, ensuring knowledge continuity.**

---

## 🌟 Overview

The Persistent Memory Agent System is designed to support long-term research and knowledge management by providing an AI assistant that can **remember past interactions and research notes for specific topics**. Unlike stateless chatbots, this system allows analysts and users to **continue where they left off** in any research session, maintaining context and building upon previous findings. It leverages local LLMs via Ollama for privacy and efficiency, with a robust FastAPI backend managing memory and interactions, and a user-friendly Streamlit frontend.

---

## ✨ Features

- **Topic-Specific Memory Persistence:** Each research topic maintains its own conversation history and summary memory using TinyDB.
- **Knowledge Continuity:** Allows users to resume past research sessions with full context.
- **Interactive Agent:** Interact with a summarizer/explainer agent that leverages the topic's memory.
- **Dynamic LLM Selection:** Choose your preferred local LLM model (e.g., Llama2, Mistral, Qwen) from the frontend.
- **Timeline of Notes & Memory Logs:** View the full conversation history for any selected topic.
- **Session Export:** Export the entire session's memory (conversation history) in JSON format for review or backup.
- **Local LLM Power:** Utilizes Ollama and LangChain to run open-source LLMs locally, ensuring data privacy and reducing reliance on external API costs.
- **Professional Backend:** A FastAPI backend handles all core logic, memory management, and LLM orchestration, providing a scalable and maintainable architecture.
- **Intuitive Frontend:** A Streamlit application provides an easy-to-use interface for managing topics and interacting with the AI.

---

## 📁 File Structure

```text
    memory-agent-system/
    ├── .env                        # Environment variables for configuration
    ├── agents/
    │   └── memory_agent.py         # Handles LLM interaction and TinyDB memory
    ├── backend/
    │   └── main.py                 # FastAPI application (API endpoints)
    ├── memory/
    │   └── memory_store.json       # TinyDB file for all topic histories
    ├── orchestrator.py             # Coordinates agents and memory flow
    ├── frontend.py                 # Streamlit user interface
    ├── requirements.txt            # Python dependencies
    └── README.md                   # Project documentation
```

---

## 🚀 Getting Started

Follow these steps to set up and run your Persistent Memory Agent System on your local machine.

### Prerequisites

1. **Ollama:**
    - Download and install Ollama from the official website: [ollama.ai](https://ollama.ai/).
    - Pull the desired LLM models:
      ```bash
      ollama pull llama2
      ollama pull qwen:4b
      ollama pull mistral
      ollama pull gemma
      ollama pull phi3
      ```
    - **Start the Ollama server:**
      ```bash
      ollama serve
      ```
      Keep this terminal window open and running.

2. **Python 3.8+:**
    - Download and install from [python.org](https://www.python.org/downloads/).

### Installation

1. **Create Project Directory:**
    ```bash
    mkdir memory-agent-system
    cd memory-agent-system
    ```

2. **Create Subdirectories:**
    ```bash
    mkdir backend agents memory
    ```

3. **Create Files:**
    - `agents/memory_agent.py`
    - `orchestrator.py`
    - `backend/main.py`
    - `frontend.py`
    - `requirements.txt`
    - `.env`
    - `README.md`

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

---

## 🏃 Running the Application

This application requires the Ollama server and a separate FastAPI backend process to be running.

1. **Start Ollama Server (Terminal 1):**
    ```bash
    ollama serve
    ```
    (Keep this terminal open.)

2. **Start FastAPI Backend (Terminal 2):**
    ```bash
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```
    (Keep this terminal open.)

3. **Run the Streamlit Frontend (Terminal 3):**
    ```bash
    streamlit run frontend.py
    ```
    (This will open the app in your browser.)

---

## 🖥️ Usage Guide

1. **Choose or Create a Topic:**  
   Use the sidebar dropdown to select or create a topic.
2. **Select LLM Model:**  
   Choose your preferred Ollama LLM model.
3. **Interact with the AI:**  
   Type your message or research note and send.
4. **View AI Response & Memory Log:**  
   The AI's response and full conversation history will appear.
5. **Export Session:**  
   Click the export button to download the topic's history as JSON.
6. **Clear Session:**  
   Use the sidebar button to reset the frontend state (does not delete persistent memory).

---

## 🧠 Project Logic and Workflow

This project uses a **client-server architecture** with a **FastAPI backend** and a **Streamlit frontend**.

### Code Workflow

1. **Frontend Initialization & Topic Management (`frontend.py`):**
    - Loads topics from `/topics/` endpoint.
    - Fetches conversation history for selected topic.

2. **User Interaction & Request to Backend:**
    - Sends user input, topic, and LLM model to `/chat/` endpoint.

3. **Backend API Handling (`backend/main.py`):**
    - Validates data and routes to orchestrator.

4. **Orchestration and LLM Initialization (`orchestrator.py`):**
    - Initializes LangChain OllamaLLM with selected model.
    - Calls agent logic and retrieves updated history.

5. **Memory Agent Logic (`agents/memory_agent.py`):**
    - Retrieves and updates topic-specific conversation history in TinyDB.
    - Constructs prompt and invokes LLM.

6. **Result Display & Export:**
    - Frontend displays AI response and history.
    - Export endpoint returns JSON data.

### File Responsibilities

- **`memory-agent-system/`**: Main entry point, orchestration, dependencies, environment, docs.
- **`backend/`**: FastAPI application (API endpoints).
- **`agents/`**: Core AI agent logic and TinyDB operations.
- **`memory/`**: Persistent conversation storage.
- **`.env`**: Environment variables.
- **`requirements.txt`**: Python dependencies.
- **`README.md`**: Documentation.

---

## 🛠️ Technologies Used

- **Python**
- **FastAPI**
- **Uvicorn**
- **Ollama**
- **LangChain**
- **LLMs (Llama2/Mistral/Gemma/Phi3/Qwen:4b)**
- **Streamlit**
- **Requests**
- **TinyDB**
- **python-dotenv**
- **JSON**

---

## 🧩 Extending & Customizing

- Add more agents (e.g., Fact-Checker, Research Agent).
- Use a more robust database for large-scale/multi-user scenarios.
- Add authentication/authorization for multi-user environments.
- Explore real-time updates or WebSockets.
- Fine-tune prompts for custom AI behaviors.
- Enhance the frontend UI/UX.

---

## ⚠️ Troubleshooting

- **Ollama connectivity issues:**  
  Ensure Ollama is running and models are pulled.
- **Backend errors:**  
  Ensure FastAPI backend is running.
- **Request timeouts:**  
  Use smaller models or ensure sufficient system resources.
- **Unsupported LLM model:**  
  Update supported models in backend/frontend.
- **Dependencies not found:**  
  Activate your virtual environment before installing.
- **Streamlit rerun errors:**  
  Use `st.rerun()` and ensure your code is updated.

---

## 💡 Tips & Best Practices

- Use a dedicated GPU for best performance.
- Keep models updated.
- Experiment with prompt templates.
- Use Git for version control.
- Store sensitive info in `.env`.

---

## 🤝 Contributing

We welcome contributions! Fork, open issues, and submit pull requests.

- **Bug Reports:** Include error messages and system details.
- **Feature Requests:** Open an issue describing your idea.
- **Pull Requests:** Ensure code is well-documented and tested.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙋 FAQ

**Q: Can I use this with other LLMs?**  
A: Yes! Any model supported by Ollama can be used. Update the model lists in the frontend and backend.

**Q: Is my data private?**  
A: Yes. All processing is local; no data is sent externally.

**Q: Can I use this for commercial research?**  
A: Yes, subject to the MIT License and the LLMs' licenses.

---

*Developed for Your Personal Use — Empower your research with local AI agents and persistent memory!*
