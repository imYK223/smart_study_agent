from typing import TypedDict, Optional

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from app.rag_chain import build_rag_chain

load_dotenv()  # loads OPENAI_API_KEY (if present)


class QAState(TypedDict):
    question: str
    answer: Optional[str]


rag_chain = build_rag_chain()


def rag_node(state: QAState) -> QAState:
    """Single node that runs the RAG chain for the given question."""
    question = state["question"]
    answer = rag_chain.invoke(question)   # <--- now returns just a string
    return {"question": question, "answer": answer}


def build_graph():
    graph = StateGraph(QAState)
    graph.add_node("rag", rag_node)
    graph.set_entry_point("rag")
    graph.add_edge("rag", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    print("Smart Study Notes Agent (LangGraph + LangChain)")
    print("Type your questions. Type 'exit' to quit.")

    while True:
        q = input("\nQuestion: ")
        if q.lower().strip() in {"exit", "quit"}:
            break

        state = {"question": q, "answer": None}
        final_state = app.invoke(state)

        print("\nAnswer:\n", final_state["answer"])
