# Dummy database using Python dicts/lists

internships = [
    {"id": 1, "title": "AI Developer Intern", "skills": ["python", "ml"]},
    {"id": 2, "title": "Web Developer Intern", "skills": ["javascript", "react"]},
    {"id": 3, "title": "Data Analyst Intern", "skills": ["python", "sql"]},
    {"id": 4, "title": "DevOps Intern", "skills": ["docker", "ci/cd"]},
]

users = {
    1: {"name": "Alice", "history": ["python", "ml"]},
    2: {"name": "Bob", "history": ["javascript", "react"]},
}

def get_all_internships():
    return internships

def get_user_history(user_id):
    user = users.get(user_id)
    return user["history"] if user else None