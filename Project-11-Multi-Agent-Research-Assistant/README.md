# 🧠 Your Personal Multi-Agent Research Assistant

> **An intelligent, privacy-first research tool powered by local LLMs and multi-agent collaboration.**

---

## 🌟 Overview

The Multi-Agent Research Assistant is designed to **automate and streamline competitive intelligence workflows** using multiple collaborating AI agents. Each agent specializes in a distinct research task, working together to deliver rapid, accurate, and comprehensive research briefs—all while running **entirely on your local machine** for maximum privacy and cost efficiency.

---

## File Structure

```Bash
    multi-agent-researcher/
    ├── .env                  # Environment variables for configuration
    ├── backend/
    │   └── main.py           # FastAPI application serving as the central API
    ├── agents/
    │   ├── search_agent.py   # Simulates web search
    │   ├── summarize_agent.py# Summarizes findings using LLM
    │   ├── checker_agent.py  # Fact-checks summary using LLM
    │   └── report_agent.py   # Generates final report using LLM
    ├── data/
    │   └── sample_research_topic.txt # Sample research topic for testing
    ├── orchestrator.py       # Coordinates the flow between different agents
    ├── frontend.py           # Streamlit user interface
    ├── requirements.txt      # Python dependencies
    └── README.md             # Project documentation

```

---

## ✨ Features

- **Delegated Research:** Accepts a research topic and delegates tasks to specialized AI agents.
- **Search Agent:** Simulates web search to gather initial findings relevant to the topic. *(Extendable to real search APIs)*
- **Summarizer Agent:** Condenses raw findings into a concise and digestible summary.
- **Fact-Checker Agent:** Reviews the generated summary for potential biases, hallucinations, or inaccuracies, providing constructive feedback.
- **Report Generator Agent:** Compiles a final, polished research brief, integrating the summary and any necessary corrections.
- **Local LLM Power:** Utilizes Ollama to run open-source LLMs (e.g., Llama2, Mistral) locally, ensuring data privacy and reducing reliance on external API costs.
- **Streamlined Workflow:** An intuitive Streamlit frontend orchestrates the entire multi-agent pipeline.
- **Downloadable Reports:** Allows users to download the complete research output in JSON format.
- **Modular & Extensible:** Easily add new agents or swap LLMs to fit your workflow.
- **Cross-Platform:** Works on Windows, macOS, and Linux.
- **No Cloud Required:** All data and computation stay on your device.

---

## 🚀 Getting Started

Follow these steps to set up and run your Multi-Agent Research Assistant on your local machine.

### Prerequisites

1. **Ollama:**
    - Download and install Ollama from the official website: [ollama.ai](https://ollama.ai/).
    - Once installed, open your terminal and pull the desired LLM model. We recommend `llama2` (as used in the agents) or `mistral` for faster runs:
      ```bash
      ollama pull llama2
      # or
      ollama pull mistral
      ```
    - Ensure Ollama is running in the background (it often runs as a service after installation).

2. **Python 3.8+:**
    - Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

3. **Streamlit:**
    - Required for the interactive frontend. Will be installed via `requirements.txt`.

### Installation

1. **Create Project Directory:**
    ```bash
    mkdir multi-agent-researcher
    cd multi-agent-researcher
    ```
2. **Create Subdirectories:**
    ```bash
    mkdir agents data
    ```
3. **Create Files:**
    - Create `data/sample_research_topic.txt` and paste the sample research topic.
    - Create `agents/search_agent.py` and paste its code.
    - Create `agents/summarize_agent.py` and paste its code.
    - Create `agents/checker_agent.py` and paste its code.
    - Create `agents/report_agent.py` and paste its code.
    - Create `orchestrator.py` in the root and paste its code.
    - Create `frontend.py` in the root and paste its code.
    - Create `requirements.txt` in the root and paste the dependencies list.
    - Create `README.md` in the root and paste this content.

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

This application requires Ollama to be actively serving the LLM model.

1. **Start Ollama LLM (Terminal 1):**  
   Open a new terminal window (and activate your virtual environment if you created one) in *any* directory and run the Ollama model you intend to use. This command keeps the model loaded and ready for requests:
    ```bash
    ollama run llama2
    # or
    ollama run mistral
    ```
   Keep this terminal window open and running.

2. **Run the Frontend (Terminal 2):**  
   Open another new terminal window (and activate your virtual environment) in the `multi-agent-researcher` directory and run:
    ```bash
    streamlit run frontend.py
    ```
   This will open the Streamlit application in your default web browser, typically at `http://localhost:8501`.

---

## 🖥️ Usage Guide

1. **Enter Research Topic:** In the Streamlit application, type your desired research topic into the input field.
2. **Run Research:** Click the "🚀 Run Research Pipeline" button. A loading spinner will appear as the agents work through the process.
3. **View Results:** Once the pipeline is complete, the simulated search results, summarized findings, fact-checker's feedback, and the final research brief will be displayed.
4. **Download:** Use the "Download All Research Results (JSON)" button to save the complete output.
5. **Clear:** Click "🧹 Clear All" to reset the input and results.

---

## 🧠 Project Logic and Workflow

This project is structured around a **multi-agent orchestration pattern**, where specialized Python modules (agents) collaborate to achieve a complex research goal. The `orchestrator.py` acts as the central coordinator, directing the flow of information and tasks between these agents.

### **Code Workflow:**

1. **User Input (`frontend.py`):**
    - The user provides a `research topic` via the Streamlit web interface.
    - When the "Run Research Pipeline" button is clicked, the `frontend.py` script calls the `run_research_pipeline` function from `orchestrator.py`, passing the research topic.

2. **Orchestration (`orchestrator.py`):**
    - The `run_research_pipeline` function initiates the sequence of operations:
        - It first calls the `run_search` function from `agents/search_agent.py`.
        - The `search_results` from the Search Agent are then passed to the `summarize_text` function from `agents/summarize_agent.py`.
        - The `summary` generated by the Summarizer Agent is passed to the `fact_check` function from `agents/checker_agent.py`.
        - Finally, both the `summary` and `corrections` (from the Fact-Checker Agent) are passed to the `generate_report` function from `agents/report_agent.py`.
        - All intermediate and final results are collected into a dictionary and returned to the `frontend.py`.
    - Error handling is implemented at each step to gracefully manage issues like Ollama connectivity or timeouts.

3. **Agent Execution (`agents/*.py`):**
    - **`search_agent.py` (Simulated Search):** This module currently contains a placeholder function `run_search` that returns pre-defined text simulating web search results. In a real-world application, this would be extended to integrate with external web search APIs (e.g., Serper, Brave Search, Google Custom Search) to fetch actual, real-time data.
    - **`summarize_agent.py` (Summarization):** This module's `summarize_text` function takes raw text (search results) and sends a specific prompt to the local LLM (via Ollama) to generate a concise summary.
    - **`checker_agent.py` (Fact-Checking):** The `fact_check` function in this module receives the generated summary. It then prompts the LLM to review the summary for potential biases, factual inaccuracies, or hallucinations, providing feedback or suggested corrections.
    - **`report_agent.py` (Report Generation):** The `generate_report` function takes the summarized findings and any fact-checker feedback. It then uses the LLM to compile a structured, professional research brief, typically including an executive summary, key findings, and considerations/caveats.

4. **Result Display (`frontend.py`):**
    - The `frontend.py` receives the complete results dictionary from the `orchestrator.py`.
    - It then renders these results in a user-friendly format within the Streamlit interface, displaying each stage of the research process (simulated search results, summary, fact-checker feedback, and the final report).
    - Download options are provided for convenience.

### **File Responsibilities:**

- **`multi-agent-researcher/` (Root Directory):** Contains the main application entry point (`frontend.py`), the orchestration logic (`orchestrator.py`), project dependencies (`requirements.txt`), and documentation (`README.md`).
- **`agents/` Directory:** Houses individual Python modules, each representing a specialized AI agent responsible for a single, distinct task (search, summarize, fact-check, report generation). This modularity makes the system easy to extend and maintain.
- **`data/` Directory:** Stores sample input files, such as `sample_research_topic.txt`, for easy testing and demonstration.
- **`requirements.txt`:** Lists all necessary Python libraries for the project, ensuring easy environment setup.
- **`README.md`:** Provides comprehensive documentation, setup instructions, usage guide, project logic, troubleshooting, and extension possibilities.

This multi-agent architecture allows for clear separation of concerns, making the system highly modular, scalable, and easier to debug compared to a monolithic AI solution.

---

## 🛠️ Technologies Used

- **Python:** The core programming language.
- **Ollama:** Platform for running open-source LLMs locally.
- **LLMs (Llama2/Mistral):** Large Language Models for text generation, summarization, and analysis.
- **Streamlit:** For building the interactive web-based user interface.
- **Requests:** Python HTTP library for making calls to the Ollama API.
- **FastAPI (for HTTPException):** Used for consistent error handling across agents, though a full FastAPI backend is not explicitly run for this project's API.
- **JSON:** For exporting and sharing research results.

---

## 🧩 Extending & Customizing

- **Add New Agents:** Create new Python modules in the `agents/` directory and register them in `orchestrator.py`.
- **Swap LLMs:** Change the model name in agent code and pull the desired model with Ollama.
- **Integrate Real Search APIs:** Replace the simulated search logic in `search_agent.py` with calls to real web search APIs (e.g., SerpAPI, Bing, Google).
- **Customize Output:** Modify `report_agent.py` to change the report format or add new sections.

---

## ⚠️ Troubleshooting

- **"Could not connect to Ollama server" / "404 Not Found":**
    - Ensure Ollama is installed and running (`ollama serve` in a separate terminal if it's not running as a service).
    - Verify that you have pulled the `llama2` (or `mistral`) model using `ollama pull llama2`.
    - Crucially, ensure you have run `ollama run llama2` (or `ollama run mistral`) in a dedicated terminal. This command loads the model into memory for serving.
    - Check if the Ollama server is running on `http://localhost:11434`. You can adjust `OLLAMA_API_BASE_URL` in agent files if needed.
- **"The analysis request timed out" / "504 Gateway Timeout":**
    - LLM inference can be slow, especially on CPU. Timeouts for Ollama calls are set to 480 seconds (8 minutes) in the agent files, and the overall orchestrator timeout in `frontend.py` is 500 seconds.
    - If timeouts persist, consider:
        - Using a smaller LLM model (e.g., a quantized version like `llama2:7b-chat-q4_0` or `mistral:7b-instruct-v0.2-q4_0`).
        - Ensuring your system has sufficient RAM (16GB+ recommended) and a dedicated GPU if possible.
        - Simplifying the research topic or the expected output from the LLMs.
- **Dependencies not found:**
    - Make sure you have activated your Python virtual environment (`source venv/bin/activate` or `.\venv\Scripts\activate`) before running `pip install -r requirements.txt`.
- **`AttributeError: module 'streamlit' has no attribute 'experimental_rerun'`:**
    - The provided code uses `st.rerun()`, which is the current correct method. Ensure your `frontend.py` is fully updated.

---

## 💡 Tips & Best Practices

- **Use a Dedicated GPU:** For best performance, run Ollama with GPU acceleration if available.
- **Keep Models Updated:** Regularly check for new or improved LLMs on [ollama.ai/library](https://ollama.ai/library).
- **Experiment with Prompts:** Tweak agent prompts for more tailored research outputs.
- **Version Control:** Use Git to track changes and collaborate with others.

---

## 🤝 Contributing

We welcome contributions! Feel free to fork this repository, open issues, and submit pull requests.

- **Bug Reports:** Please include error messages and system details.
- **Feature Requests:** Open an issue describing your idea.
- **Pull Requests:** Ensure code is well-documented and tested.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙋 FAQ

**Q: Can I use this with other LLMs?**  
A: Yes! Any model supported by Ollama can be used. Just pull and run the model, and update the agent code accordingly.

**Q: Is my data private?**  
A: Absolutely. All processing happens locally; no data is sent to external servers.

**Q: Can I use this for commercial research?**  
A: Yes, subject to the MIT License and the licenses of the LLMs you use.

---

*Developed for Your Personal Use — Empower your research with local AI agents!*

---
