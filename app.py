# app.py
import streamlit as st
import pandas as pd
import sqlite3
import os
import re
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy import create_engine, inspect
from rapidfuzz import process, fuzz
import io

# ----------------------------
# Config & Setup
# ----------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY missing in .env")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant"

DB_PATH = "nl_sql_chat_db.sqlite"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

st.set_page_config(page_title="NL → SQL Chat", layout="wide")
st.title("💬 DataSpeak – NL → SQL")

# ----------------------------
# Utilities
# ----------------------------
def to_lower_columns(df):
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def get_tables():
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [r[0] for r in cur.fetchall()]

def get_table_columns(table):
    insp = inspect(engine)
    try:
        return [c["name"] for c in insp.get_columns(table)]
    except:
        return []

def normalize_token(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def best_column_match(token, columns, thresh=60):
    if not columns:
        return None
    keys = {normalize_token(c): c for c in columns}
    best = process.extractOne(normalize_token(token), list(keys.keys()), scorer=fuzz.ratio)
    return keys[best[0]] if best and best[1] >= thresh else None

def apply_fuzzy_replace(question, columns):
    words = re.findall(r"[A-Za-z0-9_]+", question)
    fixed = question
    for w in sorted(set(words), key=len, reverse=True):
        match = best_column_match(w, columns)
        if match:
            fixed = re.sub(rf"\b{re.escape(w)}\b", match, fixed, flags=re.IGNORECASE)
    return fixed

def ask_llm_system(prompt, user_message):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_message}
    ]
    resp = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
    return resp.choices[0].message.content

def clean_sql(sql):
    # Remove Markdown code fences
    sql = re.sub(r"```[a-zA-Z]*", "", sql)
    sql = sql.replace("```", "")
    # Remove any trailing explanation
    sql = re.split(r"This SQL|This query|Explanation:", sql)[0]
    return sql.strip()

# ----------------------------
# Session State
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------
# 1️⃣ Upload New Dataset
# ----------------------------
st.subheader("Upload CSV / Excel (New Dataset)")
uploaded = st.file_uploader("Choose a file", type=["csv", "xlsx"])
if uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        df = to_lower_columns(df)
        st.write("Preview (first 5 rows)")
        st.dataframe(df.head())

        table_name = st.text_input("Table name", value=re.sub(r"\W+", "_", uploaded.name.split(".")[0]).lower())
        if st.button("Save to Database"):
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            st.success(f"Saved {len(df)} rows to table '{table_name}'")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# ----------------------------
# 2️⃣ Choose Table to Query
# ----------------------------
tables = get_tables()
if tables:
    st.markdown("---")
    st.subheader("Select Table & Ask Questions")

    table_to_query = st.selectbox("Select table to query", tables)
    cols = get_table_columns(table_to_query)
    st.write("Schema:", cols)

    question = st.text_area("Enter your question", placeholder="e.g., Show total sales per region")
    if st.button("Generate & Run SQL"):
        if question.strip():
            # Fuzzy match columns
            fixed_question = apply_fuzzy_replace(question, cols)
            system_prompt = f"""
You are an expert SQL generator for SQLite. Use ONLY these columns:
{', '.join(cols)}
TABLE: {table_to_query}

RULES:
- Output ONLY valid SQL
- Do NOT include markdown or explanation
- Do NOT invent or rename columns
"""
            try:
                gen_sql = ask_llm_system(system_prompt, fixed_question).strip()
                gen_sql = clean_sql(gen_sql)  # Remove fences/explanation
            except Exception as e:
                st.error(f"LLM error: {e}")
                gen_sql = ""

            # Store in session history
            st.session_state.history.append({
                "table": table_to_query,
                "question": question,
                "sql": gen_sql,
                "result": None
            })

            # Execute SQL
            try:
                df_res = pd.read_sql_query(gen_sql, conn)
                st.subheader("Generated SQL")
                st.code(gen_sql, language="sql")

                st.subheader("Query Result")
                st.dataframe(df_res)

                # Store CSV for download
                buf = io.StringIO()
                df_res.to_csv(buf, index=False)
                st.download_button("Download CSV", data=buf.getvalue(), file_name="query_result.csv")

                st.session_state.history[-1]["result"] = buf.getvalue()
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")

# ----------------------------
# 3️⃣ Chat History
# ----------------------------
if st.session_state.history:
    st.markdown("---")
    st.subheader("💾 Chat History (Last 10)")
    for i, item in enumerate(reversed(st.session_state.history[-10:])):
        st.write(f"Table: {item['table']}")
        st.write(f"Q: {item['question']}")
        st.code(item["sql"], language="sql")
        if item.get("result"):
            st.download_button(f"Download result #{len(st.session_state.history)-i}",
                               data=item["result"], file_name=f"result_{i}.csv")
