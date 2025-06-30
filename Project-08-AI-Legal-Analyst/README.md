# ⚖️ LexPro Legal Document Analyzer

> *Empowering legal professionals with AI-driven insights, privacy-first.*

---

![LexPro Banner](https://img.shields.io/badge/AI-Powered-blueviolet?style=for-the-badge) ![License](https://img.shields.io/github/license/hardiksankhla/legal-analyzer-lexpro?style=for-the-badge) ![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen?style=for-the-badge)

---

## 🚦 Why LexPro?

Legal documents are complex, time-consuming, and often overwhelming. LexPro Legal Document Analyzer transforms this challenge into an opportunity—extracting actionable insights, summarizing lengthy contracts, and surfacing critical clauses in seconds. Built for privacy, powered by local LLMs, and designed for legal professionals.

---

## ✨ Features

- **📝 Document Analysis:** Paste any legal document and let LexPro do the heavy lifting.
- **🔍 Concise Summarization:** Instantly get a clear, accurate summary of the document’s core content.
- **📑 Key Clause Extraction:** Automatically identifies and extracts vital clauses: *Term, Termination, Liability, Jurisdiction, Confidentiality*, and more.
- **🧠 Named Entity Recognition (NER):** Detects and categorizes parties, dates, locations, and titles.
- **🎨 User-Friendly Interface:** Intuitive Streamlit web app—no technical expertise required.
- **⚡ Robust Backend:** FastAPI ensures blazing-fast, scalable API services.
- **🔒 Local LLM Integration:** Ollama runs LLMs (Llama2, Mistral) locally—your data never leaves your machine.
- **⬇️ Downloadable Results:** Export extracted data in JSON or plain text.
- **🛡️ Privacy by Design:** No cloud, no third-party data sharing—your documents stay yours.
- **🧩 Modular & Extensible:** Easily add new clause types, models, or integrations.

---

## 🎬 Demo

![LexPro Demo GIF](https://raw.githubusercontent.com/hardiksankhla/legal-analyzer-lexpro/main/assets/demo.gif)

> *See LexPro in action: upload, analyze, and extract—all in seconds!*

---

## 🚀 Getting Started

### Prerequisites

- **Ollama:** [Download & install](https://ollama.ai/). Pull your preferred LLM:
  ```bash
  ollama pull llama2
  # or
  ollama pull mistral
  ```
- **Python 3.8+**: [Get Python](https://www.python.org/downloads/).

### Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/hardiksankhla/legal-analyzer-lexpro.git
    cd legal-analyzer-lexpro
    ```
2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

- **Backend (FastAPI):**
    ```bash
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```
- **Frontend (Streamlit):**
    ```bash
    streamlit run frontend/app.py
    ```

---

## 📝 Usage

1. **Paste Text:** Drop your legal document into the Streamlit app.
2. **Analyze:** Click "🚀 Analyze Document" and let the AI work.
3. **View Results:** Instantly see summaries, clauses, and entities.
4. **Download:** Export results as JSON or text.
5. **Clear:** Reset with "🧹 Clear All".

---

## 📁 Project Structure

```bash
LexPro-AI-Legal-Analyst/
├── backend/
│   └── main.py
├── frontend/
│   └── app.py
├── data/
│   └── example_contract.txt
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [Requests](https://requests.readthedocs.io/en/latest/)
- **Frontend:** [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/)
- **LLM:** [Ollama](https://ollama.ai/), [Llama2](https://ollama.ai/library/llama2), [Mistral](https://ollama.ai/library/mistral)

---

## 💡 Example Use Cases

- **Contract Review:** Instantly surface key obligations and risks.
- **Due Diligence:** Extract parties, dates, and jurisdictions for compliance.
- **Legal Research:** Summarize lengthy case law or statutes.
- **Education:** Help students and trainees understand legal documents.

---

## ⚠️ Troubleshooting

- **Ollama connection issues:** Ensure Ollama is running and the model is pulled.
- **Backend errors:** Confirm FastAPI is running on `localhost:8000`.
- **LLM response issues:** Try a different model or refine prompts.
- **Dependency issues:** Activate your virtual environment before installing.

---

## 🤝 Contributing

We welcome your ideas, bug reports, and pull requests!  
- Fork the repo, create a feature branch, and submit a PR.


---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

**Hardik Sankhla**  
AI Engineer | Data Scientist | Full Stack Developer | Technical Writer

Hardik Sankhla is a passionate technologist with expertise in artificial intelligence, machine learning, and full stack software development. With a strong background in building scalable AI-powered solutions, Hardik has contributed to a variety of open-source projects and enterprise applications. He specializes in natural language processing, data analytics, and cloud-native architectures.

Hardik is the founder of School of AI India and has mentored hundreds of students and professionals in AI, data science, and software engineering. He is known for his clear technical writing, engaging workshops, and commitment to democratizing AI education. Hardik regularly shares insights on AI trends, best practices, and project tutorials through his blog and social media.
 
- LinkedIn: [linkedin.com/in/hardiksankhla](https://www.linkedin.com/in/hardik-sankhla)  
- GitHub: [github.com/hardiksankhla](https://github.com/hardik-sankhla)  
- School of AI India: [schoolofai.in](https://schoolofai.in)

---

## 🌟 Acknowledgements

- Inspired by the open-source AI and legal tech communities.
- Special thanks to contributors and early testers.

---

*Developed with ❤️ by Hardik Sankhla*

> *“Turning legal complexity into clarity—one document at a time.”*
