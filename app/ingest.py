import os
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from app.config import get_embeddings  # <-- NEW


DATA_DIR = Path("data/source")
DB_DIR = Path("data/chroma_db")


def load_documents() -> List:
    docs = []
    for path in DATA_DIR.glob("**/*"):
        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            docs.extend(loader.load())
        elif path.suffix.lower() in {".txt", ".md"}:
            loader = TextLoader(str(path), encoding="utf-8")
            docs.extend(loader.load())
    if not docs:
        raise RuntimeError(f"No documents found in {DATA_DIR.resolve()}")
    return docs


def split_documents(docs: List):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    return splitter.split_documents(docs)


def build_vectorstore():
    os.makedirs(DB_DIR, exist_ok=True)

    print(f"[INFO] Loading documents from {DATA_DIR} ...")
    docs = load_documents()
    print(f"[OK] Loaded {len(docs)} raw documents/pages")

    print("[INFO] Splitting into chunks ...")
    chunks = split_documents(docs)
    print(f"[OK] Created {len(chunks)} chunks")

    print("[INFO] Building Chroma vector store ...")
    embeddings = get_embeddings()  # <-- uses OpenAI or HF automatically

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
    ).persist()

    print(f"[OK] Vector DB saved to {DB_DIR.resolve()}")


if __name__ == "__main__":
    build_vectorstore()
