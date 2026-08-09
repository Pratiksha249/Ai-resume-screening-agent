from agent.parser import extract_resume_text
from agent.extractor import extract_resume_information
from agent.embeddings import EmbeddingMatcher
from agent.scorer import CandidateScorer


# --------------------------------------------------
# 1. Load resume
# --------------------------------------------------

file_path = "data/resumes/candidate_01.txt"

resume_text = extract_resume_text(file_path)


# --------------------------------------------------
# 2. Extract candidate information
# --------------------------------------------------

candidate = extract_resume_information(resume_text)


# --------------------------------------------------
# 3. Job description
# --------------------------------------------------

job_description = """
We are looking for a Junior AI Research Associate
with knowledge of Python, machine learning,
natural language processing, deep learning,
transformer models, and generative AI.

Candidates should have at least 6 months
of relevant AI or machine learning experience.

A degree or postgraduate qualification in
Artificial Intelligence, Machine Learning,
Computer Science, or a related field is preferred.
"""


# --------------------------------------------------
# 4. Required skills
# --------------------------------------------------

required_skills = [
    "Python",
    "Machine Learning",
    "NLP",
    "Deep Learning",
    "Transformers",
    "Generative AI"
]


# --------------------------------------------------
# 5. Create embedding matcher
# --------------------------------------------------

matcher = EmbeddingMatcher()

similarity = matcher.calculate_similarity(
    job_description,
    resume_text
)

semantic_score = similarity * 100


# --------------------------------------------------
# 6. Create scorer
# --------------------------------------------------

scorer = CandidateScorer()


# --------------------------------------------------
# 7. Calculate individual scores
# --------------------------------------------------

skill_score = scorer.calculate_skill_score(
    candidate["skills"],
    required_skills
)

experience_score = scorer.calculate_experience_score(
    candidate["experience"],
    minimum_months=6
)

education_score = scorer.calculate_education_score(
    candidate["education"],
    [
        "Artificial Intelligence",
        "Machine Learning"
    ]
)


# --------------------------------------------------
# 8. Calculate overall score
# --------------------------------------------------

overall_score = scorer.calculate_overall_score(
    semantic_score,
    skill_score,
    experience_score,
    education_score
)


# --------------------------------------------------
# 9. Display results
# --------------------------------------------------

print("=" * 60)
print("CANDIDATE SCORING")
print("=" * 60)

print(f"\nCandidate: {candidate['name']}")

print(f"\nSemantic Score:    {semantic_score:.2f}/100")
print(f"Skills Score:      {skill_score:.2f}/100")
print(f"Experience Score:  {experience_score:.2f}/100")
print(f"Education Score:   {education_score:.2f}/100")

print("-" * 60)

print(f"Overall Score:     {overall_score:.2f}/100")