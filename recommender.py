# import sqlite3
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import faiss

# # Load embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # ----------------------------
# # Load jobs from database
# # ----------------------------
# def load_jobs():
#     conn = sqlite3.connect("jobs.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT id, title, description, skills FROM jobs
#     """)
#     rows = cursor.fetchall()

#     conn.close()
#     return rows


# # ----------------------------
# # Prepare FAISS index
# # ----------------------------
# jobs_data = load_jobs()

# # Extract fields
# job_ids = [row[0] for row in jobs_data]
# job_titles = [row[1] for row in jobs_data]
# job_skills = [row[3] for row in jobs_data]

# # Encode job skills
# job_embeddings = model.encode(job_skills, convert_to_numpy=True)

# dim = job_embeddings.shape[1]

# # Create index
# index = faiss.IndexFlatL2(dim)
# index.add(job_embeddings.astype("float32"))


# # ----------------------------
# # Recommendation Function
# # ----------------------------
# def recommend_jobs(user_skills, top_k=3):
#     # Encode user skills
#     user_emb = model.encode([user_skills], convert_to_numpy=True).astype("float32")

#     # Search
#     distances, indices = index.search(user_emb, top_k)

#     results = []
#     for rank, idx in enumerate(indices[0]):
#         results.append({
#             "id": job_ids[idx],
#             "title": job_titles[idx],
#             "skills": job_skills[idx],
#             "distance": float(distances[0][rank])
#         })

#     return results
#################################################################################################
# import sqlite3
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import faiss

# # Initialize the sentence transformer model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Load jobs from the database
# def load_jobs():
#     conn = sqlite3.connect("jobs.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, title, description, skills FROM jobs")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# jobs_data = load_jobs()
# job_ids = [row[0] for row in jobs_data]
# job_titles = [row[1] for row in jobs_data]
# job_skills = [row[3] for row in jobs_data]

# # Encode job skills into embeddings
# job_embeddings = model.encode(job_skills)
# dim = job_embeddings.shape[1]

# # Build FAISS index
# index = faiss.IndexFlatL2(dim)
# index.add(np.array(job_embeddings, dtype='float32'))

# # Recommend jobs based on user skills
# def recommend_jobs(user_skills, top_k=3):
#     if not user_skills.strip():
#         return []

#     user_emb = model.encode([user_skills])
#     distances, indices = index.search(np.array(user_emb, dtype='float32'), top_k)
    
#     results = []
#     for i, idx in enumerate(indices[0]):
#         results.append({
#             "id": job_ids[idx],
#             "title": job_titles[idx],
#             "skills": job_skills[idx],
#             "distance": float(distances[0][i])
#         })
#     return results
###############################################################################################
# Last_virsion
# import sqlite3
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import faiss

# # Initialize Sentence Transformer model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Load jobs from database
# def load_jobs():
#     conn = sqlite3.connect("jobs.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, title, description, skills FROM jobs")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# jobs_data = load_jobs()
# job_ids = [row[0] for row in jobs_data]
# job_titles = [row[1] for row in jobs_data]
# job_skills = [row[3] for row in jobs_data]

# # Encode job skills into embeddings
# job_embeddings = model.encode(job_skills)
# dim = job_embeddings.shape[1]

# # Build FAISS index
# index = faiss.IndexFlatL2(dim)
# index.add(np.array(job_embeddings, dtype='float32'))

# # Recommend jobs based on user skills
# def recommend_jobs(user_skills, top_k=3):
#     user_emb = model.encode([user_skills])
#     distances, indices = index.search(np.array(user_emb, dtype='float32'), top_k)
    
#     results = []
#     for i, idx in enumerate(indices[0]):
#         results.append({
#             "id": job_ids[idx],
#             "title": job_titles[idx],
#             "skills": job_skills[idx],
#             "distance": distances[0][i]
#         })
#     return results

# # Save user viewed jobs history
# def save_history(username, jobs):
#     conn = sqlite3.connect("jobs.db")
#     cursor = conn.cursor()
#     for job in jobs:
#         cursor.execute("INSERT INTO history (username, job_id) VALUES (?, ?)", (username, job['id']))
#     conn.commit()
#     conn.close()

# # Get user history
# def get_user_history(username):
#     conn = sqlite3.connect("jobs.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT j.title, j.skills FROM jobs j
#         JOIN history h ON j.id = h.job_id
#         WHERE h.username = ?
#     """, (username,))
#     rows = cursor.fetchall()
#     conn.close()
#     return [{"title": row[0], "skills": row[1]} for row in rows]
##############################################################################################
import sqlite3
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os

# --- Initialize SentenceTransformer ---
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- Database paths ---
DB_PATH = "jobs.db"
HISTORY_DB = "history.db"
USERS_DB = "users.db"

# --- Jobs functions ---
def load_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, skills FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    return rows

jobs_data = load_jobs()
job_ids = [row[0] for row in jobs_data]
job_titles = [row[1] for row in jobs_data]
job_skills = [row[3] for row in jobs_data]

job_embeddings = model.encode(job_skills)
dim = job_embeddings.shape[1]

index = faiss.IndexFlatL2(dim)
index.add(np.array(job_embeddings, dtype='float32'))

def recommend_jobs(user_skills, top_k=5):
    user_emb = model.encode([user_skills])
    distances, indices = index.search(np.array(user_emb, dtype='float32'), top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "id": job_ids[idx],
            "title": job_titles[idx],
            "skills": job_skills[idx],
            "distance": distances[0][i]
        })
    return results

# --- History functions ---
def init_history_db():
    conn = sqlite3.connect(HISTORY_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            user TEXT,
            job_id INTEGER,
            job_title TEXT,
            skills TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_history(user, job):
    conn = sqlite3.connect(HISTORY_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (user, job_id, job_title, skills) VALUES (?, ?, ?, ?)",
                   (user, job['id'], job['title'], job['skills']))
    conn.commit()
    conn.close()

def get_user_history(user):
    conn = sqlite3.connect(HISTORY_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT job_title, skills FROM history WHERE user=?", (user,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Users functions ---
def init_users_db():
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(username, password):
    conn = sqlite3.connect(USERS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

