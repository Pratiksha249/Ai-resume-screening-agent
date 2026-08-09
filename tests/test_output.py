from agent.pipeline import ResumeScreeningAgent
from agent.output import ResultsExporter


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


# Create screening agent
agent = ResumeScreeningAgent()


# Screen candidates
results = agent.screen_candidates(
    resume_folder="data/resumes",
    job_description=job_description
)


# Export results
exporter = ResultsExporter()

output_path = exporter.export_csv(
    results["candidates"]
)


print("=" * 60)
print("RESULTS EXPORTED SUCCESSFULLY")
print("=" * 60)

print(f"\nFile created at:")
print(output_path)