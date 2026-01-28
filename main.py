import streamlit as st
from sql_engine import answer_question
from langchain_groq import ChatGroq

# =====================================================
# App Configuration
# =====================================================
st.set_page_config(
    page_title="GenAI SQL Assistant",
    layout="centered"
)

# =====================================================
# Sidebar Navigation
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "💬 Ask Questions"]
)

# =====================================================
# Forbidden (Write / DDL) Intents
# =====================================================
FORBIDDEN_INTENTS = [
    "create table",
    "create a table",
    "write table",
    "write a table",
    "insert",
    "update",
    "delete",
    "drop table",
    "alter table",
    "truncate",
    "create schema",
    "modify",
    "change",
    "alter"
]

# =====================================================
# Meta / Conversational Responses (Hybrid Mode)
# =====================================================
META_RESPONSES = {
    "who are you": "I’m a GenAI-powered SQL assistant designed to help you explore a music store database using natural language.",
    "who created you": "I was built as a GenAI project to demonstrate natural-language querying over structured data.",
    "who made you": "I was created as part of a GenAI SQL assistant project.",
    "what can you do": "I can answer analytical questions about artists, customers, albums, and sales from the database.",
    "what are you": "I’m a read-only data analysis assistant that answers questions using SQL behind the scenes.",
    "you are not making any sense": "Sorry about that. Please ask a clear question related to the database, and I’ll help."
}

# =====================================================
# Vague / Underspecified Inputs
# =====================================================
VAGUE_INPUTS = [
    "what",
    "why",
    "how",
    "what?",
    "why?",
    "how?",
    "for what",
    "for what?",
    "tell me more",
    "explain",
    "huh",
    "?"
]

# =====================================================
# 🏠 HOME / LANDING PAGE
# =====================================================
if page == "🏠 Home":

    st.title("🤖 GenAI SQL Assistant")

    st.markdown(
        """
### What is this application?

This is an **AI-powered data assistant** that allows you to ask questions in **plain English**
and get answers directly from a structured SQL database — without writing SQL.

The assistant:
- Understands your question
- Converts it into a SQL query
- Executes it safely on the database
- Explains the result clearly and concisely

This tool is designed for **data exploration and analysis**, not for modifying data.
"""
    )

    st.markdown("---")

    st.markdown(
        """
### 📊 About the Dataset (Chinook Database)

This application uses the **Chinook database**, a public sample database that represents
a **digital music store**.

It contains information about:
- 🎵 Artists and albums
- 🎧 Tracks and genres
- 👥 Customers
- 🧾 Invoices and sales transactions

You can think of it as a simplified version of an online music platform’s backend database.
"""
    )

    st.markdown("---")

    st.markdown(
        """
### ✅ What kind of questions can you ask?

You can ask **read-only, analytical questions**, such as:

- *Who is the most profitable artist?*
- *Which customers have spent the most money?*
- *How many customers are there in each country?*
- *What are the top-selling genres?*
- *Which albums generated the highest revenue?*

The assistant works best with **specific, business-style questions**.
"""
    )

    st.markdown("---")

    st.markdown(
        """
### 🚫 What this assistant cannot do

For safety reasons, the assistant **cannot**:
- Create or modify tables
- Insert, update, or delete data
- Change database structure or schema

It is strictly a **read-only analytics assistant**.
"""
    )

    st.markdown("---")

    st.info(
        "👉 Use the **Ask Questions** tab in the sidebar to start exploring the data."
    )

# =====================================================
# 💬 CHAT / QUESTION PAGE
# =====================================================
else:

    st.title("💬 Ask Questions")
    st.caption("Ask questions in English. Powered by LLaMA 3.3 + Groq.")

    # -----------------------------
    # Chat State Initialization
    # -----------------------------
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Render chat history
    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    question = st.chat_input("Ask a question about the database")

    if question:
        st.chat_message("user").write(question)

        lowered_question = question.lower().strip()

        # -----------------------------
        # Meta / Conversational Handling
        # -----------------------------
        for key, response in META_RESPONSES.items():
            if key in lowered_question:
                st.chat_message("assistant").write(response)

                st.session_state.chat.extend([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": response}
                ])

                st.stop()

        # -----------------------------
        # Vague / Underspecified Input Handling
        # -----------------------------
        if (
            len(lowered_question.split()) <= 2
            or lowered_question in VAGUE_INPUTS
        ):
            clarification_message = (
                "I need a bit more detail to help you. "
                "Please ask a specific question about the database, "
                "such as artists, customers, albums, or sales."
            )

            st.chat_message("assistant").write(clarification_message)

            st.session_state.chat.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": clarification_message}
            ])

            st.stop()

        # -----------------------------
        # Forbidden Intent Guardrail
        # -----------------------------
        if any(intent in lowered_question for intent in FORBIDDEN_INTENTS):
            refusal_message = (
                "I can’t create, modify, or delete database tables or data. "
                "This assistant is designed strictly for read-only data analysis. "
                "Please ask questions about existing data."
            )

            st.chat_message("assistant").write(refusal_message)

            st.session_state.chat.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": refusal_message}
            ])

            st.stop()

        # -----------------------------
        # Core SQL + Explanation Flow
        # -----------------------------
        with st.spinner("Thinking..."):
            sql, cols, rows = answer_question(question)

            explainer = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0
            )

            explanation_prompt = f"""
You are a data analyst answering a business question.

Rules:
- Answer the question directly in the first sentence.
- Do NOT explain columns, schema, or SQL mechanics.
- Do NOT speculate, hedge, or use uncertainty language.
- Do NOT include meta commentary.
- Be concise and confident.
- If a numeric value exists, include it.
- If there is exactly one result row, state it clearly.
- If multiple rows exist, summarize patterns briefly in one sentence.

Question:
{question}

Query Result:
Columns: {cols}
Rows: {rows}

Answer:
"""

            explanation = explainer.invoke(explanation_prompt).content.strip()

        # -----------------------------
        # Render Assistant Response
        # -----------------------------
        st.chat_message("assistant").write(explanation)

        st.session_state.chat.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": explanation}
        ])
