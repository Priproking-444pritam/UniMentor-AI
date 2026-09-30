"""
UniMentor AI - Agent Workflow (LangGraph)
=========================================
Workflow:

    START
      |
      v
    router node      -> manager agent picks the category
      |
      v
    retrieve node    -> fetch chunks from that department only
      |
      +-- no relevant chunks --> fallback node --> END
      |
      v
    answer node      -> specialist agent writes a grounded answer
      |
      v
     END

The conditional edge after retrieval is what stops the system
from hallucinating: if nothing relevant was found, the LLM is
never asked to answer at all.
"""

from typing import List, TypedDict

from langgraph.graph import END, START, StateGraph

from agents import generate_answer, manager_agent
from config import CATEGORY_TO_DEPARTMENT, NOT_FOUND_MESSAGE, TOP_K
from rag import build_context, retrieve


# ============================================================
# STATE
# ============================================================

class AgentState(TypedDict):
    question: str
    history: List[dict]
    category: str
    reason: str
    context: str
    sources: list
    answer: str


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state):
    """Manager agent decides which specialist handles the question."""
    category, reason = manager_agent(state["question"])

    return {
        "category": category,
        "reason": reason,
    }


# ============================================================
# RETRIEVE NODE
# ============================================================

def retrieve_node(state, chunks, metadata, index):
    """Fetch relevant chunks from the selected department."""
    department = CATEGORY_TO_DEPARTMENT[state["category"]]

    results = retrieve(
        state["question"],
        chunks,
        metadata,
        index,
        department=department,
        top_k=TOP_K,
    )

    # If a department search finds nothing, widen the search to
    # all documents once before giving up.
    if not results and department is not None:
        results = retrieve(
            state["question"],
            chunks,
            metadata,
            index,
            department=None,
            top_k=TOP_K,
        )

    context, sources = build_context(results)

    return {
        "context": context,
        "sources": sources,
    }


# ============================================================
# CONDITIONAL EDGE
# ============================================================

def has_context(state):
    """Decide whether there is enough evidence to answer."""
    if state["context"].strip():
        return "answer"

    return "fallback"


# ============================================================
# ANSWER NODE
# ============================================================

def answer_node(state):
    """Specialist agent writes the grounded answer."""
    answer = generate_answer(
        state["question"],
        state["context"],
        state["category"],
        state.get("history"),
    )

    return {"answer": answer}


# ============================================================
# FALLBACK NODE
# ============================================================

def fallback_node(state):
    """Used when retrieval returned nothing relevant."""
    return {
        "answer": NOT_FOUND_MESSAGE,
        "sources": [],
    }


# ============================================================
# GRAPH BUILDER
# ============================================================

def create_graph(chunks, metadata, index):
    """
    Build and compile the LangGraph workflow. The retrieval
    resources are closed over by a wrapper so they do not have
    to be carried inside the state.
    """
    graph = StateGraph(AgentState)

    def retrieve_wrapper(state):
        return retrieve_node(state, chunks, metadata, index)

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------
    graph.add_node("router", router_node)
    graph.add_node("retrieve", retrieve_wrapper)
    graph.add_node("answer", answer_node)
    graph.add_node("fallback", fallback_node)

    # --------------------------------------------------------
    # Edges
    # --------------------------------------------------------
    graph.add_edge(START, "router")
    graph.add_edge("router", "retrieve")

    graph.add_conditional_edges(
        "retrieve",
        has_context,
        {
            "answer": "answer",
            "fallback": "fallback",
        },
    )

    graph.add_edge("answer", END)
    graph.add_edge("fallback", END)

    return graph.compile()
