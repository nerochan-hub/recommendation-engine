from database import internships

def recommend_internships(user_history):
    # Simple content-based filtering on skill overlap
    recommendations = []
    for internship in internships:
        if set(internship["skills"]) & set(user_history):
            recommendations.append(internship)
    return recommendations