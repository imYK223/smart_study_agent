# 📘 Smart Study Agent  
### *A LangGraph + LangChain RAG Agent with Automatic OpenAI / Local LLM Switching + Optional Streamlit GUI*

---

## 🌟 Overview

**Smart Study Agent** is an intelligent, document-aware assistant built using:

- **LangChain** → document loading, embeddings, retrieval  
- **LangGraph** → agent workflow orchestration  
- **ChromaDB** → vector database  
- **OpenAI or Ollama** → LLM backend (auto-selected)  
- **HuggingFace embeddings** → local fallback  
- **Streamlit GUI (optional)** → clean chat interface  

Upload multiple PDFs → the system ingests them → then ask questions like:

- “Summarize Chapter 3”
- “Explain this concept simply”
- “Give me bullet-point notes”
- “Compare topic A vs topic B”

This project showcases **LLM orchestration, RAG pipelines, embeddings, agents, vector search, and multimodal ingestion**—perfect for your AI/ML portfolio.

---

## 🚀 Features

### 🔍 Retrieval-Augmented Generation (RAG)
Semantic search + contextual answers directly from user documents.

### 🔄 Automatic Backend Switching

| Condition | LLM Backend | Embeddings |
|----------|-------------|------------|
| `.env` has API key | OpenAI GPT models | OpenAIEmbeddings |
| No API key / quota | Ollama (local) | HuggingFace MiniLM |

### 🆓 100% Free Local Mode
Works offline using:

- **Ollama + llama3**  
- **HuggingFace all-MiniLM-L6-v2 embeddings**

### 🧩 Modular Architecture
- Ingestion pipeline  
- RAG chain  
- LangGraph agent  
- Vector DB  
- Optional GUI  

### 🖥️ Streamlit Web GUI (Optional)
A modern chat-style web interface to replace the terminal.

---

## 🧩 Architecture

```
                ┌──────────────────────────┐
                │       User Question      │
                └──────────────┬───────────┘
                               ▼
                     ┌─────────────────┐
                     │   LangGraph     │
                     │    Agent        │
                     └───────┬─────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │       RAG Pipeline       │
                │  (Runnable Composition)  │
                └───────┬──────────┬───────┘
                        │          │
                        ▼          ▼
            ┌────────────────┐   ┌────────────────┐
            │ Retriever      │   │ Prompt Builder │
            └──────┬─────────┘   └────────────────┘
                   ▼
         ┌──────────────────────┐
         │ LLM (OpenAI/Ollama)  │
         └──────────────────────┘
                   ▼
          ┌────────────────────┐
          │    Final Answer    │
          └────────────────────┘
```

---

## 📁 Project Structure

```
smart_study_agent/
│
├── main.py                     # LangGraph terminal agent
├── ui_app.py                   # Streamlit GUI
│
├── app/
│   ├── config.py               # OpenAI vs Local backend switch
│   ├── ingest.py               # PDF → Chroma ingestion
│   ├── rag_chain.py            # RAG pipeline using Runnables
│
├── data/
│   ├── source/                 # User PDF uploads
│   └── chroma_db/              # Vector database
│
├── .env.example
├── .gitignore
├── requirements.txt
├── install_dependencies.sh
└── README.md
```

---

# 🛠️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/imYK223/smart_study_agent.git
cd smart_study_agent
```

## 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
./install_dependencies.sh
```

Or manually:

```bash
pip install -r requirements.txt
```

## 4. (Optional) Install GUI dependencies

```bash
pip install streamlit
```

---

# 🔌 Backends: OpenAI or Local (Automatic)

## ✅ Option A — Use OpenAI (recommended for best quality)

1. Create a `.env` file (look at `.env.example`):

```env
OPENAI_API_KEY=sk-your-key-here
```

2. Run the application — it will automatically use:

- `ChatOpenAI`
- `OpenAIEmbeddings`

### 🔑 OpenAI Setup (Optional — for Best Model Quality)

If you want to use OpenAI models (GPT-4.1, GPT-4o, etc.) instead of the free local LLM, follow these steps:

#### ⭐ How to Get an OpenAI API Key
1. Visit: https://platform.openai.com/account/api-keys  
2. Log in with your OpenAI account  
3. Click **"Create new secret key"**  
4. Copy the key (it looks like: `sk-xxxxxx...`)

#### ⭐ Add Your Key to the Project
Create a `.env` file in the project root:

---

## 🆓 Option B — Fully Local Mode (no API key)

If `.env` does *not* contain an API key, the system switches to:

- **LLM:** Ollama (`llama3` - size: 4.3GB, runs locally)  
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`) 

### Install Ollama:

```bash
brew install ollama
ollama pull llama3
```

Ollama auto-runs in the background on macOS; you typically do **not** need to call `ollama serve` manually.

---

# 📥 Step 1: Ingest Your Documents

Place PDFs or TXT files into:

```text
data/source/
```

Then run:

```bash
python -m app.ingest
```

This builds the Chroma vector DB.

---

# 🤖 Step 2: 
## A. Run the Streamlit Web GUI (Recommended)

```bash
streamlit run ui_app.py
```

This launches a browser-based interface at:

```text
http://localhost:8501
```

You can upload PDFs, rebuild the index, and chat with the agent in a chat-like UI.

---
## B. Run the Smart Study Agent (Terminal Mode)

```bash
python main.py
```

This starts a simple CLI where you can type questions and get answers based on your documents.

---



## 🖥️ Choosing Between GUI Mode and Terminal Mode

The project provides **two independent ways** to interact with the Smart Study Agent:

### 1️⃣ Streamlit GUI (Recommended)
Run:

```bash
streamlit run ui_app.py
```

- No need to run `main.py` beforehand  
- Upload PDFs directly from the browser  
- Rebuild the index with a button  
- Chat-style interface with history  
- Best option for day-to-day usage and demos  

### 2️⃣ Terminal Agent (CLI via LangGraph)

Run:

```bash
python main.py
```

- Uses the same RAG + LangGraph backend  
- Useful for debugging, quick tests, or when you prefer the terminal  
- No GUI required  

Both modes are **independent** — you can use either one at any time.

---

# 🧪 Troubleshooting

### ❌ `Connection refused http://localhost:11434`
Ollama is not running.  
Fix:

```bash
open -a Ollama
```

---

### ❌ `listen tcp 127.0.0.1:11434: bind: address already in use`
Ollama is already running in the background — you do **not** need to run `ollama serve` manually.  Check with `curl http://localhost:11434/api/tags` or restart Ollama using `pkill -f Ollama && open -a Ollama`.

---

### ❌ “No documents found”
Add your files to:

```text
data/source/
```

Then rebuild the index:

```bash
python -m app.ingest
```

---

### ❌ OpenAI quota error (429)
You are out of OpenAI API credits.  
Remove `OPENAI_API_KEY` from `.env` → the system automatically switches to **local mode** (Ollama + HuggingFace embeddings).

---

# 📈 Roadmap

- [x] Multi-PDF ingestion  
- [x] Automatic backend switching  
- [x] Local LLM support (llama3)  
- [x] Streamlit GUI  
- [ ] FastAPI REST backend  
- [ ] Web deployment (HuggingFace Spaces)  
- [ ] Multi-agent LangGraph workflow  
- [ ] Document citation extraction  

---

# 🤝 Contributing

PRs and suggestions are welcome!

---

# ⭐ If this project helps you, please consider starring the repo!
