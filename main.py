import streamlit as st
from sql_engine import answer_question
from langchain_groq import ChatGroq

st.set_page_config(page_title="GenAI SQL Assistant", layout="centered")

st.title("🤖 GenAI SQL Assistant")
st.caption("Ask questions in English. Powered by LLaMA 3.3 + Groq.")

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.chat_input("Ask a question about the database")

if question:
    st.chat_message("user").write(question)

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
- Do NOT include meta commentary (e.g., "based on the data").
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

    st.chat_message("assistant").write(explanation)

    st.session_state.chat.extend([
        {"role": "user", "content": question},
        {"role": "assistant", "content": explanation}
    ])
