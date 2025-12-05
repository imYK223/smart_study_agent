#!/bin/bash

echo "======================================="
echo "  Smart Study Agent - Setup Script"
echo "======================================="

# ---- Step 1: Create Virtual Environment ----
echo "[INFO] Creating virtual environment (.venv)..."

python3 -m venv .venv

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment."
    exit 1
fi

echo "[INFO] Virtual environment created."

# ---- Step 2: Activate Virtual Environment ----
echo "[INFO] Activating virtual environment..."

# Mac/Linux
source .venv/bin/activate

# # Windows (Git Bash / WSL users)
# # source .venv/Scripts/activate

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment."
    exit 1
fi

echo "[INFO] Virtual environment activated."

# ---- Step 3: Install Dependencies ----
echo "[INFO] Installing dependencies..."

pip install --upgrade pip

pip install \
    langchain \
    langchain-openai \
    langgraph \
    chromadb \
    python-dotenv \
    langchain-community \
    sentence-transformers \
    pypdf \
    langchain-text-splitters \ 

if [ $? -ne 0 ]; then
    echo "[ERROR] Dependency installation failed."
    deactivate
    exit 1
fi

echo "[INFO] All dependencies installed."

# ---- Step 4: Create folder structure ----
echo "[INFO] Creating project folders for data..."

mkdir -p data/source

echo "[INFO] Folder structure ready."

echo "[INFO] Setup complete! Run your project with:"
echo ""
echo "  source .venv/bin/activate"
echo "  python -m app.ingest"
echo ""
echo "======================================="
