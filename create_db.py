import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    skills TEXT
)
""")

# Insert sample jobs
cursor.executemany("""
INSERT INTO jobs (title, description, skills)
VALUES (?, ?, ?)
""", [
    ("Data Scientist", "Analyze data & build ML models", "python, machine learning, pandas, sklearn"),
    ("AI Engineer", "Build and deploy AI systems", "deep learning, transformers, pytorch, python"),
    ("Software Engineer", "Develop backend systems", "python, sql, problem solving, algorithms"),
    ("Data Analyst", "Analyze reports and dashboards", "excel, power bi, sql, visualization")
])

conn.commit()
conn.close()

print("Database created successfully!")
