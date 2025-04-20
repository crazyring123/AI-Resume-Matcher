import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        match_score REAL,
        job_description TEXT,
        resume_text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# Insert resume data into the database
def insert_resume(name, email, match_score, job_description, resume_text):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO resumes (name, email, match_score, job_description, resume_text)
    VALUES (?, ?, ?, ?, ?)
    """, (name, email, match_score, job_description, resume_text))
    conn.commit()
    conn.close()

# Fetch all resumes
def fetch_all_resumes():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes")
    rows = cursor.fetchall()
    conn.close()
    return rows


