from langchain_core.prompts import PromptTemplate

SQL_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an expert SQL engineer.

Generate ONE valid SQLite SQL query.

Rules:
- Use ONLY provided schema
- Output ONLY SQL
- No markdown, no comments
- SQLite compatible

Schema:
{schema}

Question:
{question}

SQL:
"""
)

FIX_PROMPT = PromptTemplate(
    input_variables=["schema", "question", "sql", "error"],
    template="""
Fix the SQL query using the schema and error.

Rules:
- Output ONLY SQL
- No markdown

Schema:
{schema}

Question:
{question}

Failed SQL:
{sql}

Error:
{error}

Corrected SQL:
"""
)
