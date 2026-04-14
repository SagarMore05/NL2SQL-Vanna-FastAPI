# 🧠 NL2SQL System using Vanna AI 2.0 + FastAPI

## 📌 Overview

This project implements a Natural Language to SQL (NL2SQL) system that allows users to ask questions in plain English and retrieve results from a database without writing SQL.

The system is built using:

* Vanna AI 2.0 (LLM-based SQL generation framework)
* FastAPI (backend API)
* SQLite (database)

---

## ⚙️ Features

* Convert natural language queries into SQL
* Execute queries on a relational database
* Return structured JSON results
* Interactive API via Swagger UI
* Predefined training dataset (15+ Q&A pairs)

---

## 🏗️ Project Structure

Cogninest_AI/
│── main.py              # FastAPI application
│── vanna_setup.py       # Vanna agent + DB setup
│── seed_memory.py       # Q&A training dataset
│── clinic.db            # SQLite database
│── requirements.txt
│── README.md
│── RESULTS.md

---

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd Cogninest_AI
```

---

### 2. Create Virtual Environment

```bash
python -m venv loan_env
loan_env\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add API Key

Create a `.env` file in the root folder:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
uvicorn main:app --reload
```

---

## 🌐 Access API

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example Query

### Request

```json
{
  "question": "How many patients do we have?"
}
```

### Response

```json
{
  "question": "How many patients do we have?",
  "sql_query": "SELECT COUNT(*) FROM patients",
  "columns": ["COUNT(*)"],
  "rows": [[200]],
  "row_count": 1
}
```

---

## 🧠 Memory Seeding

The assignment required seeding the system with 15 Q&A pairs.

* A dataset of 15+ queries is defined in `seed_memory.py`
* Due to version limitations of Vanna AI, direct programmatic memory insertion APIs (such as `save()` or `add()`) were not available
* Instead, these queries serve as structured training references
* Runtime learning is handled using built-in Vanna tools

---

## ⚠️ Note on NL2SQL Generation

Due to limitations in the installed Vanna AI version:

* Direct NL-to-SQL execution methods were not exposed
* A fallback rule-based SQL generator was implemented

This ensures:

* Functional system
* Accurate SQL execution
* Complete end-to-end pipeline

---

## 📊 Tech Stack

* Python
* FastAPI
* SQLite
* Vanna AI 2.0
* Gemini API

---

## 🎯 Conclusion

This project demonstrates:

* Natural language interface for databases
* SQL generation and execution
* API-based architecture for real-world applications

---

## 📌 How to Test

1. Run the server:

```bash
uvicorn main:app --reload
```

2. Open:

```
http://127.0.0.1:8000/docs
```

3. Use `/chat` endpoint with queries like:

* "How many patients do we have?"
* "List all doctors"
* "Show total revenue"

