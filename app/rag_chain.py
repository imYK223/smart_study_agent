# from pathlib import Path

# from langchain_community.vectorstores import Chroma
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain

# from app.config import get_embeddings, get_llm  # <-- NEW


# DB_DIR = Path("data/chroma_db")


# def get_retriever(k: int = 4):
#     embeddings = get_embeddings()  # <-- OpenAI or HF
#     vectordb = Chroma(
#         embedding_function=embeddings,
#         persist_directory=str(DB_DIR),
#     )
#     return vectordb.as_retriever(search_kwargs={"k": k})


# def build_rag_chain():
#     llm = get_llm()  # <-- OpenAI or Ollama

#     system_prompt = """You are a helpful study assistant.
# You ONLY use the provided context to answer.
# If the answer is not in the context, say you don't know.

# Always:
# - Answer clearly and concisely
# - Use bullet points where helpful
# - Mention which document or section you used if possible.
# """

#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", system_prompt),
#             ("human", "Question:\n{input}\n\nContext:\n{context}"),
#         ]
#     )

#     doc_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
#     retriever = get_retriever()

#     rag_chain = create_retrieval_chain(retriever, doc_chain)
#     return rag_chain


# if __name__ == "__main__":
#     chain = build_rag_chain()

#     while True:
#         q = input("\nAsk a study question (or 'exit'): ")
#         if q.lower() in {"exit", "quit"}:
#             break
#         result = chain.invoke({"input": q})
#         print("\nAnswer:\n", result["answer"])
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.config import get_embeddings, get_llm


DB_DIR = Path("data/chroma_db")


def get_retriever(k: int = 20):
    """
    Build a retriever on top of the persisted Chroma DB.
    Uses either OpenAI or HuggingFace embeddings (see config.get_embeddings).
    """
    embeddings = get_embeddings()
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=str(DB_DIR),
    )
    return vectordb.as_retriever(search_kwargs={"k": k})


def build_rag_chain():
    """
    Build a simple RAG pipeline using the new LangChain runnable style:

       question (str)
         -> {"input": question, "context": retriever(question)}
         -> prompt
         -> LLM
         -> string answer
    """
    retriever = get_retriever()
    llm = get_llm()

    system_prompt = """You are a helpful study assistant.

You primarily use the provided context to answer.
If the answer clearly requires information far beyond the context,
do your best with what you have instead of complaining about missing pages.

If the user asks to "summarize the whole PDF" or "summarize the whole document",
produce the best high-level summary you can from the available context.
Do NOT say that you only see a few pages; instead, act as if you are summarizing
the key ideas you can observe.

Always:
- Answer clearly and concisely
- Use bullet points where helpful
- Mention which concepts, chapters, or sections you see in the context if possible.
"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Question:\n{input}\n\nContext:\n{context}"),
        ]
    )

    # This builds the flow:
    # input question (string) -->
    #   {"input": question, "context": retriever(question)} -->
    #   prompt.format(...) -->
    #   llm -->
    #   string
    rag_chain = (
        {
            "input": RunnablePassthrough(),   # pass the question as "input"
            "context": retriever,             # retriever(question) -> docs
        }
        | prompt
        | llm
        | StrOutputParser()                   # make sure we get back a plain string
    )

    return rag_chain


if __name__ == "__main__":
    chain = build_rag_chain()

    while True:
        q = input("\nAsk a study question (or 'exit'): ")
        if q.lower() in {"exit", "quit"}:
            break
        answer = chain.invoke(q)  # now we just pass the question string
        print("\nAnswer:\n", answer)
