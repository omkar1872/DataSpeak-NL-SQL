#  DataSpeak – Natural Language → SQL with Streamlit + Groq + SQLite

> **Ask questions in English → Get SQL + Results instantly.**  
> DataSpeak transforms natural language into executable SQL using Groq’s Llama-3.1 model, safely runs it on SQLite, and displays results in an interactive Streamlit UI.

---

# 🔍 Project Overview

**DataSpeak** is a full-stack Intelligent NL → SQL engine designed to help analysts, data scientists, and developers query datasets without writing SQL manually.

Users simply upload a CSV/Excel file and ask questions like:

> “Show total sales by region”  
> “Top 10 products by revenue”  
> “Average age of employees older than 40”

The system:

1. Reads and cleans the dataset  
2. Normalizes column names  
3. Uses **RapidFuzz** to fix spelling mistakes  
4. Uses **Groq Llama-3.1-8B** to generate SQL  
5. Executes SQL on **SQLite**  
6. Shows results, SQL, and downloadable CSV  
7. Stores history of last 10 queries  

This is a **portfolio-grade** ML + Data Engineering + LLM project designed to impress recruiters.

---

# 🧠 Why This Project Is Valuable

✔️ Solves a real business problem (NL → SQL automation)  
✔️ Uses modern AI tools (Groq LLM, RapidFuzz, Streamlit)  
✔️ Includes database engineering (SQLite + SQLAlchemy)  
✔️ Demonstrates prompt engineering  
✔️ Demonstrates full-stack deployment  
✔️ Strong evidence of **AI/ML + software engineering** skills  

This is the kind of project hiring managers love.

---

# 🏗️ Architecture
```
       ┌──────────────────┐
       │ User Query (NL)  │
       └─────────┬────────┘
                 ↓
    ┌──────────────────────────┐
    │ Fuzzy Column Matching    │  ← RapidFuzz fixes typos
    └─────────┬────────────────┘
              ↓
    ┌──────────────────────────┐
    │  Groq LLM (Llama 3.1)    │  ← Generates optimized SQL
    └─────────┬────────────────┘
              ↓
    ┌──────────────────────────┐
    │    SQL Cleaning Layer    │
    └─────────┬────────────────┘
              ↓
    ┌──────────────────────────┐
    │     SQLite Engine        │  ← Executes SQL safely
    └─────────┬────────────────┘
              ↓
    ┌──────────────────────────┐
    │ Streamlit UI Response    │  ← Table + SQL + CSV download
    └──────────────────────────┘
```

---

# 🧰 Tools & Libraries — Detailed Explanation

### **1. Streamlit**
- Used to build the UI frontend  
- Handles uploads, inputs, layout, results table  
- Perfect for AI demos and rapid data apps  

**Streamlit features used:**
- `st.file_uploader`
- `st.text_input`
- `st.dataframe`
- `st.download_button`
- `st.session_state`

### **2. Groq Llama-3.1**
The heart of the system.  
Why Groq?

- Extremely fast inference  
- Deterministic SQL output  
- Great for structured generation  

A strict system prompt ensures SQL-only, no hallucinations, and no invalid columns.

### **3. RapidFuzz**
Maps user-typed tokens to valid columns:

Example:  
User writes:  
`totl sles by regon`

Mapped to:  
- `total_sales`  
- `region`

This improves SQL correctness dramatically.

### **4. Pandas**
- Loads CSV/XLSX  
- Converts SQL results to DataFrame  
- Supports CSV downloads  

### **5. SQLite**
Used because:

- Zero configuration  
- Portable  
- Fast  
- Fits perfectly for data apps  

Each uploaded dataset becomes a new SQL table.

### **6. SQLAlchemy**
- Safely executes SQL  
- Prevents injection  
- Converts results to Pandas  

### **7. python-dotenv**
Loads `.env` securely to protect your API keys.

---

# 📂 Project File Structure
```
DataSpeak/
├── app.py # Main Application
├── requirements.txt # Dependencies
├── README.md # Documentation
└── .gitignore # Ignore venv, db, env, etc.
```

⚠️ Ignore auto-generated DB files:  
- `nl_sql_chat_db.sqlite`  
- `database.db`

⚠️ Never commit `.env`.

---

# 📦 Installation

### 1️⃣ Clone

```bash
git clone https://github.com/your-username/DataSpeak.git
cd DataSpeak
```
### 2️⃣ Create venv
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  (Mac/Linux)
```
### 4️⃣ Add Groq API key
```bash
GROQ_API_KEY=your_groq_api_key
```
### ▶️ Run the App
```bash
streamlit run app.py
```
#### Visit:
```bash
http://localhost:8501

```

## 📸 Output Screenshots

Below are the actual outputs and UI screens from the DataSpeak – NL → SQL application:

<p align="center">
  <img src="./output.png" alt="Output Screenshot 1" width="95%" />
</p>

<p align="center">
  <img src="./output_1.png" alt="Output Screenshot 2" width="95%" />
</p>

<p align="center">
  <img src="./output_2.png" alt="Output Screenshot 3" width="95%" />
</p>

<p align="center">
  <img src="./output_3.png" alt="Output Screenshot 4" width="95%" />
</p>





  

