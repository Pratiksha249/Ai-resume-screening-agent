from agent.jd_analyzer import JobDescriptionAnalyzer


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


analyzer = JobDescriptionAnalyzer()

requirements = analyzer.analyze(
    job_description
)


print("=" * 60)
print("JOB DESCRIPTION ANALYSIS")
print("=" * 60)

print("\nRequired Skills:")

for skill in requirements["required_skills"]:
    print(f"  • {skill}")

print(
    "\nMinimum Experience:",
    requirements["minimum_experience_months"],
    "months"
)

print("\nEducation Keywords:")

for keyword in requirements["education_keywords"]:
    print(f"  • {keyword}")