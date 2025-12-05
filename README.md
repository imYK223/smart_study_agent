# 📘 Smart Study Agent  
### *A LangGraph + LangChain RAG Agent with Automatic OpenAI / Local LLM Switching*

---

## 🌟 Overview

**Smart Study Agent** is an intelligent, document-aware assistant built using:

- **LangChain** → document loading, embeddings, retrieval  
- **LangGraph** → agent workflow  
- **ChromaDB** → vector database  
- **OpenAI or Ollama** → LLM backend  
- **HuggingFace embeddings** (fallback when no API key is provided)

Upload your PDFs or text notes → the agent ingests them → then ask it:

- “Summarize Chapter 3”
- “Explain this in simple words”
- “Give bullet-point notes”
- “Compare Topic A and Topic B”

This project demonstrates **RAG**, **agentic reasoning**, and **backend flexibility**, making it ideal for ML/AI portfolio use.

---

## 🚀 Features

### 🔍 Retrieval-Augmented Generation (RAG)
The agent retrieves relevant text chunks from your documents and produces grounded answers.

### 🔄 Automatic Backend Switching
No setup required:

| Condition | LLM Backend | Embeddings |
|----------|-------------|------------|
| **OPENAI_API_KEY is set** | OpenAI GPT Models | OpenAIEmbeddings |
| **No API key** | Local **Ollama** Model (llama3, phi3, etc.) | HuggingFace MiniLM |

### 🆓 100% Free Local Mode
If you don’t set an OpenAI key, the system defaults to:

- **Ollama** (“llama3” by default)  
- **HuggingFace all-MiniLM-L6-v2 (local embeddings)**

### 🧩 Modular Architecture
- Ingestion pipeline  
- RAG chain (Runnable graph)  
- LangGraph agent node  
- Easily expandable  

### 🧠 Clean, modern LangChain v0.2+ API
Uses the latest Runnable & LangGraph patterns.

---

## 🧩 Architecture

```
                ┌──────────────────────────┐
                │       User Question      │
                └──────────────┬───────────┘
                               ▼
                     ┌─────────────────┐
                     │   LangGraph     │
                     │  (rag_node)     │
                     └───────┬─────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │       RAG Pipeline       │
                │  (Runnable composition)  │
                └───────┬──────────┬───────┘
                        │          │
                        ▼          ▼
            ┌────────────────┐   ┌────────────────┐
            │ Retriever      │   │ Prompt Builder │
            │ (ChromaDB)     │   └────────────────┘
            └──────┬─────────┘
                   ▼
         ┌──────────────────────┐
         │ LLM (OpenAI/Ollama)  │
         └──────────────────────┘
                   ▼
          ┌────────────────────┐
          │   Final Answer     │
          └────────────────────┘
```

---

## 📁 Project Structure

```
smart_study_agent/
│
├── main.py                   # LangGraph agent
│
├── app/
│   ├── config.py             # OpenAI vs Local (Ollama) backend switch
│   ├── ingest.py             # PDF/Text → ChromaDB vectorstore
│   ├── rag_chain.py          # RAG pipeline using Runnables
│
├── data/
│   ├── source/               # Put your PDFs here
│   └── chroma_db/            # Auto-generated vector DB
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
git clone https://github.com/your-username/smart_study_agent
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

### Install & Run Ollama

1. Download Ollama: https://ollama.com  
2. Pull a model:

```bash
ollama pull llama3
```

3. Start server:

```bash
ollama serve
```

---

# 📥 Step 1: Ingest Your Documents

Place PDFs or text files in:

```
data/source/
```

Then run:

```bash
python -m app.ingest
```

This will:

- Load PDFs  
- Split text into chunks  
- Create embeddings  
- Save them inside `data/chroma_db/`  

---

# 🤖 Step 2: Run the Smart Study Agent

```bash
python main.py
```

Example interaction:

```
Question: summarize chapter 3
Answer: ...
```

Examples you can try:

- summarize chapter 3  
- explain rigid body transformations  
- list 5 key points from chapter 2  
- compare foundation pose and classical methods  

---

# 🧪 Troubleshooting

### ❌ Error: `Connection refused http://localhost:11434`
You are in **local mode**, but Ollama is not running.

Fix:

```bash
ollama serve
```

---

### ❌ Error: `Listen tcp 127.0.0.1:11434: bind: address already in use` 
This means Ollama is already running in the background — you do NOT need to run `ollama serve` manually.  
Check with `curl http://localhost:11434/api/tags` or restart Ollama using `pkill -f Ollama && open -a Ollama`.
 
---

### ❌ “No documents found”
Ensure your files are inside:

```
data/source/
```

---

### ❌ Irrelevant RAG output  
Try adjusting:

- Chunk size  
- Chunk overlap  
- More source documents  

---

# 📈 Roadmap (Future Enhancements)

- [ ] REST API (FastAPI)  
- [ ] Web UI (Streamlit / React)  
- [ ] Multi-agent LangGraph workflow  
- [ ] PDF citation extraction  
- [ ] Online document upload  
- [ ] Reranking & semantic filtering  

---

# 🤝 Contributing
PRs and suggestions are welcome!

---

# ⭐ If you find this project useful, please consider starring the repo!
