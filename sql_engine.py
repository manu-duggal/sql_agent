import re
import sqlalchemy
from sqlalchemy import create_engine, inspect
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from prompts import SQL_PROMPT, FIX_PROMPT
from cache import get_cached, save_cache

engine = create_engine("sqlite:///Chinook_Sqlite.sqlite")

def get_schema():
    inspector = inspect(engine)
    blocks = []
    for t in inspector.get_table_names():
        cols = inspector.get_columns(t)
        blocks.append(
            f"Table: {t}\nColumns: " +
            ", ".join(f"{c['name']} ({c['type']})" for c in cols)
        )
    return "\n\n".join(blocks)

schema_text = get_schema()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def sanitize(sql):
    if sql.startswith("```"):
        sql = re.sub(r"```sql|```", "", sql, flags=re.I)
    return sql.strip().rstrip(";")

def execute(sql):
    with engine.connect() as conn:
        res = conn.execute(sqlalchemy.text(sql))
        return res.keys(), res.fetchall()

def answer_question(question, retries=2):
    cached = get_cached(question)
    sql = cached["sql"] if cached else sanitize(
        (SQL_PROMPT | llm | StrOutputParser()).invoke(
            {"schema": schema_text, "question": question}
        )
    )

    for _ in range(retries + 1):
        try:
            cols, rows = execute(sql)
            if not cached:
                save_cache(question, sql)
            return sql, cols, rows
        except Exception as e:
            sql = sanitize(
                (FIX_PROMPT | llm | StrOutputParser()).invoke({
                    "schema": schema_text,
                    "question": question,
                    "sql": sql,
                    "error": str(e)
                })
            )

    raise RuntimeError("SQL failed after retries")
