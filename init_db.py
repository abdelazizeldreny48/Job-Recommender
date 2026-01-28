import sqlite3

# Connect to SQLite database (it will create the file if not exists)
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create jobs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    skills TEXT NOT NULL
)
""")

# Insert initial jobs
jobs = [
    (1, "Data Scientist", "Analyze data and build ML models", "Python;Machine Learning;Pandas;SQL"),
    (2, "Backend Developer", "Build APIs and backend systems", "Python;Django;REST;SQL"),
    (3, "AI Researcher", "Research new AI models and implement prototypes", "Python;PyTorch;Deep Learning;NLP"),
    (4, "Frontend Developer", "Build web interfaces", "JavaScript;React;HTML;CSS")
]

cursor.executemany("INSERT OR IGNORE INTO jobs VALUES (?, ?, ?, ?)", jobs)
conn.commit()
conn.close()
print("Database initialized successfully.")
