from agent.embeddings import EmbeddingMatcher


job_description = """
We are looking for a Junior AI Research Associate
with knowledge of Python, machine learning,
natural language processing, deep learning,
and transformer models.
"""


resume = """
I am a graphic designer specializing in
Adobe Photoshop, illustration, branding,
video editing, and visual design.
"""


matcher = EmbeddingMatcher()

similarity = matcher.calculate_similarity(
    job_description,
    resume
)


print("=" * 60)
print("SEMANTIC MATCHING TEST")
print("=" * 60)

print(f"Similarity Score: {similarity:.4f}")
print(f"Similarity Percentage: {similarity * 100:.2f}%")