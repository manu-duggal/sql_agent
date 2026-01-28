import streamlit as st
from sql_engine import answer_question
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

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

        explanation = (StrOutputParser() | explainer).invoke(
            f"Explain this result conversationally:\nColumns: {cols}\nRows: {rows}"
        )

    st.chat_message("assistant").write(explanation)

    st.session_state.chat.extend([
        {"role": "user", "content": question},
        {"role": "assistant", "content": explanation}
    ])
