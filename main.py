from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# Import agent + sql_runner
from vanna_setup import sql_runner

app = FastAPI()

# -----------------------------
# Request Model
# -----------------------------
class QueryRequest(BaseModel):
    question: str


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": "connected"
    }


# -----------------------------
# SQL Generator (Basic Logic)
# -----------------------------
def simple_sql_generator(question: str):
    q = question.lower()

    if "patients" in q and ("count" in q or "how many" in q):
        return "SELECT COUNT(*) FROM patients"

    if "doctors" in q:
        return "SELECT name, specialization FROM doctors"

    if "revenue" in q:
        return "SELECT SUM(total_amount) FROM invoices"

    if "appointments" in q:
        return "SELECT * FROM appointments LIMIT 10"

    return None


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: QueryRequest):
    try:
        question = request.question

        # Step 1: Generate SQL (fallback logic)
        sql_query = simple_sql_generator(question)

        if not sql_query:
            return {
                "message": "❌ Could not understand the question",
                "question": question
            }

        # Step 2: Execute SQL
        conn = sqlite3.connect("clinic.db")
        cursor = conn.cursor()

        cursor.execute(sql_query)
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        conn.close()

        return {
            "question": question,
            "sql_query": sql_query,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }

    except Exception as e:
        return {
            "error": str(e)
        }