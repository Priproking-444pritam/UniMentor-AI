"""
UniMentor AI - Streamlit Application
====================================
Run with:
    streamlit run app.py
"""

import streamlit as st

from config import AGENT_NAMES, DEPARTMENTS, DOCUMENTS_FOLDER
from graph import create_graph
from rag import build_index, create_chunks, load_documents

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="UniMentor AI",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 UniMentor AI")
st.caption(
    "Multi-Agent Academic Advisory System — curriculum, "
    "placement and scholarship questions answered from "
    "official university documents."
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ready" not in st.session_state:
    st.session_state.ready = False


# ============================================================
# KNOWLEDGE BASE
# ============================================================

@st.cache_resource(show_spinner=False)
def initialize_knowledge_base():
    """
    Load documents, chunk them, build the FAISS index and
    compile the agent graph. Cached so this heavy work runs
    only once per session.
    """
    documents = load_documents(DOCUMENTS_FOLDER)

    if not documents:
        raise ValueError(
            "No documents found. Add PDF or TXT files inside "
            "documents/curriculum, documents/placement and "
            "documents/scholarship."
        )

    chunks, metadata = create_chunks(documents)
    index = build_index(chunks)
    graph = create_graph(chunks, metadata, index)

    return documents, chunks, metadata, index, graph


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("Knowledge Base")

    if st.button("Load / Rebuild Documents", use_container_width=True):
        initialize_knowledge_base.clear()

        with st.spinner("Reading documents and building the index..."):
            try:
                documents, chunks, metadata, index, graph = (
                    initialize_knowledge_base()
                )
                st.session_state.ready = True
                st.success("Knowledge base ready.")

            except Exception as error:
                st.session_state.ready = False
                st.error(str(error))

    if st.session_state.ready:
        documents, chunks, metadata, index, graph = (
            initialize_knowledge_base()
        )

        st.metric("Document pages", len(documents))
        st.metric("Text chunks", len(chunks))

        st.subheader("Agents")
        for category, name in AGENT_NAMES.items():
            st.write(f"• {name}")

        st.subheader("Departments")
        for department in DEPARTMENTS:
            count = sum(
                1
                for item in metadata
                if item["department"] == department
            )
            st.write(f"• {department.title()} — {count} chunks")

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Answers are grounded in the uploaded documents only.")


# ============================================================
# MAIN AREA
# ============================================================

if not st.session_state.ready:
    st.info(
        "Click **Load / Rebuild Documents** in the sidebar to build "
        "the knowledge base before asking a question."
    )

    st.subheader("Example questions")
    st.write(
        "- How many credits are required to graduate?\n"
        "- What is the minimum CGPA for placement eligibility?\n"
        "- What is the deadline for the merit scholarship?\n"
        "- Can I sit for a second company after getting placed?"
    )

else:
    documents, chunks, metadata, index, graph = (
        initialize_knowledge_base()
    )

    # --------------------------------------------------------
    # Chat history
    # --------------------------------------------------------
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("agent"):
                st.caption(f"Handled by: {message['agent']}")

            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.write(
                            f"• {source['source']} "
                            f"(page {source['page']}, "
                            f"{source['department']})"
                        )

    # --------------------------------------------------------
    # Chat input
    # --------------------------------------------------------
    question = st.chat_input("Ask an academic question...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Routing to the right agent..."):
                try:
                    result = graph.invoke(
                        {
                            "question": question,
                            "history": st.session_state.messages,
                        }
                    )

                    agent = AGENT_NAMES[result["category"]]
                    answer = result["answer"]
                    sources = result.get("sources", [])

                    st.caption(f"Handled by: {agent}")
                    st.markdown(answer)

                    if sources:
                        with st.expander("Sources"):
                            for source in sources:
                                st.write(
                                    f"• {source['source']} "
                                    f"(page {source['page']}, "
                                    f"{source['department']})"
                                )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "agent": agent,
                            "sources": sources,
                        }
                    )

                except Exception as error:
                    st.error(f"Something went wrong: {error}")
