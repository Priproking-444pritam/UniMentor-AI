"""
UniMentor AI - Agents
=====================
Contains every LLM-facing function in the system:

    Manager Agent     -> decides which specialist should answer
    Curriculum Agent  -> syllabus, credits, electives, exams
    Placement Agent   -> eligibility, drives, preparation
    Scholarship Agent -> schemes, deadlines, documents

The specialist agents share one grounded-answer function but
are given different personas and instructions through the
prompt, which is what makes each one behave differently.
"""

import json
import re

from groq import Groq

from config import (
    AGENT_NAMES,
    GROQ_API_KEY,
    MODEL,
    NOT_FOUND_MESSAGE,
)

client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# JSON PARSER
# ============================================================

def parse_json(content):
    """
    Parse JSON returned by the model, tolerating markdown
    code fences and stray text around the object.
    """
    content = content.strip()
    content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"^```\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1:
            return json.loads(content[start:end + 1])

        raise ValueError("Invalid JSON returned by the model.")


# ============================================================
# MANAGER AGENT (ROUTER)
# ============================================================

def manager_agent(question):
    """
    Classify a student question into exactly one category.
    This decides which specialist agent and which document
    set will be used for the answer.
    """
    prompt = f"""
You are the manager agent of UniMentor AI, a university
academic advisory system.

Classify the student's question into exactly one category:

CURRICULUM  - syllabus, subjects, credits, electives,
              exams, attendance, grading, semester rules
PLACEMENT   - placement eligibility, CGPA cut-offs, company
              drives, internships, resume and interview
              preparation, placement policy
SCHOLARSHIP - scholarships, fee waivers, financial aid,
              eligibility, deadlines, required documents
GENERAL     - anything else, or a question that spans
              more than one category

Student question:
{question}

Return ONLY JSON in this exact format:
{{
    "category": "CURRICULUM",
    "reason": "one short sentence"
}}

Do not answer the question. Only classify it.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an accurate question routing agent.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    try:
        result = parse_json(response.choices[0].message.content)
        category = result.get("category", "GENERAL").upper()
        reason = result.get("reason", "")

    except ValueError:
        category = "GENERAL"
        reason = "Could not classify the question reliably."

    if category not in AGENT_NAMES:
        category = "GENERAL"

    return category, reason


# ============================================================
# SPECIALIST AGENTS (GROUNDED ANSWER)
# ============================================================

AGENT_INSTRUCTIONS = {
    "CURRICULUM": (
        "Explain academic rules precisely. Always state credit "
        "values, subject codes and semester numbers exactly as "
        "they appear in the documents."
    ),
    "PLACEMENT": (
        "State eligibility criteria, CGPA cut-offs, backlog rules "
        "and deadlines exactly as written. Never soften or "
        "estimate a criterion."
    ),
    "SCHOLARSHIP": (
        "State eligibility, amounts, deadlines and required "
        "documents exactly as written. Never guess a deadline."
    ),
    "GENERAL": (
        "Answer using whichever documents are relevant and clearly "
        "indicate which area the information came from."
    ),
}


def generate_answer(question, context, category, history=None):
    """
    Generate an answer that is grounded strictly in the
    retrieved university documents.
    """
    agent_name = AGENT_NAMES[category]
    instruction = AGENT_INSTRUCTIONS[category]

    conversation = ""

    if history:
        recent = history[-4:]
        conversation = "\n".join(
            f"{turn['role'].upper()}: {turn['content']}"
            for turn in recent
        )

    prompt = f"""
You are the {agent_name} of UniMentor AI, an academic advisory
system for university students.

{instruction}

RULES:
- Answer using ONLY the university documents provided below.
- Do not use outside knowledge and do not assume anything.
- If the documents do not contain enough information, reply
  with exactly this sentence:
  "{NOT_FOUND_MESSAGE}"
- Never invent CGPA cut-offs, deadlines, credit values,
  scholarship amounts or company names.
- Mention the source file and page for the key facts you use.

RECENT CONVERSATION:
{conversation if conversation else "None"}

STUDENT QUESTION:
{question}

UNIVERSITY DOCUMENT CONTEXT:
{context}

Structure your reply as:
1. Direct answer
2. Key details (use bullet points where useful)
3. Sources

Keep the tone helpful, clear and student-friendly.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded academic advisory assistant. "
                    "You never fabricate institutional information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content
