# UniMentor AI — Multi-Agent Academic Advisory System

UniMentor AI helps university students get accurate, document-grounded answers
to academic and career questions. Instead of a single chatbot, a **manager
agent** classifies each question and routes it to the correct specialist agent,
which then retrieves information only from its own document set and generates a
grounded answer with source citations.

---

## 1. Architecture

```
                              STUDENT
                                 |
                                 v
                        Streamlit Chat UI
                                 |
                                 v
                        Manager Agent (Router)
                                 |
              +------------------+------------------+
              |                  |                  |
              v                  v                  v
      Curriculum Agent    Placement Agent   Scholarship Agent
              |                  |                  |
              +------------------+------------------+
                                 |
                                 v
                    Department-Filtered Retriever
                                 |
                                 v
                      FAISS Vector Search
                                 |
                  +--------------+--------------+
                  |                             |
          relevant chunks found          nothing relevant
                  |                             |
                  v                             v
             Groq LLM                    Fallback Node
                  |                             |
                  v                             |
         Grounded Answer                        |
         + Source Citation                      |
                  |                             |
                  +--------------+--------------+
                                 |
                                 v
                              RESPONSE
```

---

## 2. Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Application logic |
| Streamlit | Chat user interface |
| Groq API (Llama 3.3 70B) | LLM inference |
| Sentence Transformers | Text embeddings (all-MiniLM-L6-v2) |
| FAISS | Vector similarity search |
| PyPDF | PDF text extraction |
| LangGraph | Multi-agent workflow and state |
| RAG | Grounding answers in documents |
| python-dotenv | API key management |

---

## 3. Project Structure

```
UniMentor-AI/
│
├── app.py                  Streamlit interface
├── config.py               Keys, model and constants
├── rag.py                  Loading, chunking, embedding, retrieval
├── agents.py               Manager agent and specialist agents
├── graph.py                LangGraph workflow
├── requirements.txt
├── .env                    (create this yourself)
├── .env.example
├── .gitignore
├── README.md
│
└── documents/
    ├── curriculum/
    │   └── academic_regulations.txt
    ├── placement/
    │   └── placement_policy.txt
    └── scholarship/
        └── scholarship_guidelines.txt
```

Sample documents are included so the project runs immediately. Replace them
with your own institute PDFs — both `.pdf` and `.txt` files are supported.

---

## 4. Setup

**Step 1 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 2 — Add your API key**

Create a file named `.env` in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key from the Groq Console at https://console.groq.com

**Step 3 — Run the application**

```bash
streamlit run app.py
```

**Step 4 — Build the knowledge base**

Click **Load / Rebuild Documents** in the sidebar, then ask a question.

---

## 5. Sample Questions

| Question | Routed to |
| --- | --- |
| How many credits do I need to graduate? | Curriculum Agent |
| What is the minimum attendance to sit for exams? | Curriculum Agent |
| What CGPA do I need for campus placements? | Placement Agent |
| Can I appear for another company after being placed? | Placement Agent |
| What is the deadline for the merit scholarship? | Scholarship Agent |
| Can I hold two scholarships at the same time? | Scholarship Agent |

---

## 6. How Hallucination Is Prevented

1. **Department filtering** — the router restricts retrieval to one document
   set, so placement rules can never leak into a scholarship answer.
2. **Similarity threshold** — chunks scoring below `SIMILARITY_THRESHOLD` in
   `config.py` are discarded before they ever reach the LLM.
3. **Conditional fallback node** — if retrieval returns nothing relevant, the
   graph skips the LLM entirely and returns a fixed "not found" message.
4. **Strict prompting** — each specialist agent is instructed to use only the
   supplied context and never to invent CGPA cut-offs, deadlines or amounts.
5. **Source citation** — every answer lists the file and page it came from, so
   the student can verify it.

---

## 7. Configuration

All tunable values live in `config.py`:

| Setting | Default | Effect |
| --- | --- | --- |
| `CHUNK_SIZE` | 700 | Characters per chunk |
| `CHUNK_OVERLAP` | 100 | Overlap between chunks |
| `TOP_K` | 5 | Chunks sent to the LLM |
| `SIMILARITY_THRESHOLD` | 0.25 | Minimum relevance score |
| `MODEL` | llama-3.3-70b-versatile | Groq model |

---

## 8. Possible Extensions

- Add a Hostel and Administration agent for a fourth department
- Cache the FAISS index to disk so restarts are instant
- Add a feedback button on each answer to log unanswered questions
- Support Hindi and Odia queries by translating before retrieval
- Deploy on Streamlit Community Cloud with the key stored in secrets
