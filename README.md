# GenAI SQL Assistant

An AI-powered, read-only SQL assistant that allows users to ask **natural language questions**
and receive **accurate, conversational answers** directly from a structured database — without writing SQL.

🔗 **Live App:**    
👉 [Click here to access the deployed application](https://md-sqlagent.streamlit.app)


---

## 📌 Overview

This project demonstrates how **Generative AI** can be combined with **SQL databases**
to build an intelligent analytics assistant.

The system:
- Accepts questions in plain English
- Converts them into valid SQL queries
- Executes queries safely on a database
- Explains results in a clear, analyst-style response
- Prevents unsafe or write operations

The application is deployed as a **Streamlit web app** and is designed to be:
- Safe
- Explainable
- Scalable
- Easy to use for non-technical users

---

## Project Goals

- Remove the barrier of writing SQL for data exploration
- Provide accurate, explainable answers from structured data
- Ensure database safety with strict read-only constraints
- Build a real-world GenAI application suitable for deployment

---

## Dataset: Chinook Database

This application uses the **Chinook database**, a widely used public sample database that models
a **digital music store**.

### The dataset includes:
- 🎵 Artists
- 💿 Albums
- 🎧 Tracks
- 👥 Customers
- 🧾 Invoices and sales data
- 🌍 Customer geography

You can think of it as a simplified backend of an online music streaming or digital sales platform.

This makes it ideal for:
- Revenue analysis
- Customer insights
- Product performance questions

---

## How the System Works

1. **User asks a question in English**
2. **LLM converts the question to SQL**
   - Uses schema-aware prompting
   - Ensures SQLite compatibility
3. **SQL is executed safely**
   - Read-only queries only
   - No schema or data modification allowed
4. **Results are explained**
   - Answer-first
   - Concise and confident
   - Analyst-style tone
5. **Query caching**
   - Reuses validated SQL for repeated questions
   - Improves speed and efficiency

---

## System Architecture
<pre>
User (Browser)
↓
Streamlit Frontend
↓
LangChain + Groq (LLaMA 3.3)
↓
SQL Generation & Validation
↓
SQLite Database (Chinook)
↓
Result Explanation (LLM)
↓
User-Friendly Answer
</pre>

---

## Safety & Guardrails

This assistant is intentionally **read-only**.

### It CANNOT:
- Create or modify tables
- Insert, update, or delete records
- Alter schema or database structure

Any such requests are intercepted and politely refused to ensure:
- Data integrity
- Safe deployment
- Predictable behavior

---

## Example Questions You Can Ask

- Who is the most profitable artist?
- Which customers have spent the most money?
- What are the top-selling genres?
- How many customers are there in each country?
- Which albums generated the highest revenue?

The assistant works best with **specific, analytical questions**.

---

## Tech Stack

- **Frontend:** Streamlit
- **LLM:** LLaMA 3.3 (70B) via Groq
- **Framework:** LangChain
- **Database:** SQLite (Chinook)
- **Backend:** Python
- **Deployment:** Streamlit Community Cloud

---

## Project Structure

<pre>
genai-sql-assistant/
│
├── main.py # Streamlit app (UI + orchestration)
├── sql_engine.py # SQL generation, execution, retries
├── prompts.py # Prompt templates
├── cache.py # Query caching logic
├── Chinook_Sqlite.sqlite # Database file
│
├── requirements.txt
├── .gitignore
├── README.md
</pre>

---

## Running the Project Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/genai-sql-assistant.git
cd genai-sql-assistant
```
### 2️⃣ Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```
### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Set environment variable
```
export GROQ_API_KEY="your_api_key_here"   # macOS / Linux
set GROQ_API_KEY=your_api_key_here        # Windows
```
### 5️⃣ Run the app
```
streamlit run main.py
```
