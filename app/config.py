import os
from dotenv import load_dotenv

load_dotenv()  # Load .env if present

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def use_openai() -> bool:
    """
    Returns True if an OpenAI API key is configured, else False.
    """
    return bool(OPENAI_API_KEY)


def get_embeddings():
    """
    Returns an embedding model.
    - If OPENAI_API_KEY is set: OpenAIEmbeddings
    - Else: HuggingFaceEmbeddings (free, local)
    """
    if use_openai():
        from langchain_openai import OpenAIEmbeddings

        print("[CONFIG] Using OpenAIEmbeddings (requires OpenAI API key).")
        return OpenAIEmbeddings()
    else:
        from langchain_community.embeddings import HuggingFaceEmbeddings

        print("[CONFIG] Using HuggingFaceEmbeddings: all-MiniLM-L6-v2 (free/local).")
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_llm():
    """
    Returns an LLM chat model.
    - If OPENAI_API_KEY is set: ChatOpenAI
    - Else: ChatOllama (local, via Ollama server)
    """
    if use_openai():
        from langchain_openai import ChatOpenAI

        print("[CONFIG] Using OpenAI Chat model (ChatOpenAI).")
        return ChatOpenAI(
            model="gpt-4.1-mini",  # adjust if needed
            temperature=0.2,
        )
    else:
        from langchain_community.chat_models import ChatOllama

        print("[CONFIG] Using local Ollama model: llama3.")
        return ChatOllama(
            model="llama3",  # must be pulled via `ollama pull llama3`
            temperature=0.2,
        )
