import os
from pathlib import Path

import streamlit as st

from app.ingest import build_vectorstore
from app.rag_chain import build_rag_chain

# Where to save uploaded PDFs
UPLOAD_DIR = Path("data/source")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@st.cache_resource
def get_rag_chain():
    """Build and cache the RAG chain (so it doesn't rebuild on every question)."""
    return build_rag_chain()


def save_uploaded_files(files):
    """Save uploaded files into data/source/ so ingest.py can find them."""
    for f in files:
        file_path = UPLOAD_DIR / f.name
        with open(file_path, "wb") as out:
            out.write(f.getbuffer())
    return len(files)


def main():
    st.set_page_config(
        page_title="Smart Study Agent",
        page_icon="📘",
        layout="wide",
    )

    st.title("📘 Smart Study Agent")
    st.caption("RAG + LangGraph + LangChain • Multi-PDF Study Assistant")

    # Sidebar: ingestion + backend info
    with st.sidebar:
        st.header("📂 Documents")
        uploaded_files = st.file_uploader(
            "Upload PDFs or text files",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            if st.button("Save & Rebuild Index"):
                count = save_uploaded_files(uploaded_files)
                with st.spinner(f"Ingesting {count} file(s) and rebuilding vector store..."):
                    build_vectorstore()
                # Clear cached chain so it reloads with new vector DB
                get_rag_chain.clear()  # type: ignore
                st.success("Vector store rebuilt successfully!")

        st.markdown("---")
        st.subheader("ℹ️ How it works")
        st.write(
            "1. Upload one or more PDFs/notes\n"
            "2. Click **Save & Rebuild Index**\n"
            "3. Ask questions in the main panel\n"
            "4. The agent uses RAG over your documents"
        )

    # Main chat area
    st.subheader("💬 Ask questions about your documents")

    # Simple chat-like interface
    if "history" not in st.session_state:
        st.session_state.history = []  # list of (user, assistant)

    # Show history
    for user_msg, bot_msg in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(user_msg)
        with st.chat_message("assistant"):
            st.markdown(bot_msg)

    # New question input
    question = st.chat_input("Type your question (e.g., 'Summarize chapter 3')")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chain = get_rag_chain()
                try:
                    answer = chain.invoke(question)
                except Exception as e:
                    answer = f"⚠️ Error while answering: `{e}`"

                st.markdown(answer)

        st.session_state.history.append((question, answer))


if __name__ == "__main__":
    main()
