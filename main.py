from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the AI embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Example job description
job_description = """
We are looking for a Python developer with experience in
machine learning, NLP, and data science.
"""

# Example resume
resume = """
I have experience developing Python applications,
machine learning models, NLP systems, and data analysis projects.
"""

# Convert both texts into embeddings
jd_embedding = model.encode([job_description])
resume_embedding = model.encode([resume])

# Calculate similarity
similarity = cosine_similarity(
    jd_embedding,
    resume_embedding
)[0][0]

print("Job Description:")
print(job_description)

print("\nResume:")
print(resume)

print("\nSemantic Similarity Score:", round(similarity, 4))
print("Similarity Percentage:", round(similarity * 100, 2), "%")