from agent.pipeline import ResumeScreeningAgent


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


agent = ResumeScreeningAgent()


results = agent.screen_candidates(
    resume_folder="data/resumes",
    job_description=job_description
)


# --------------------------------------------------
# Show JD requirements discovered by the agent
# --------------------------------------------------

requirements = results["requirements"]

print("\n")
print("=" * 70)
print("JOB REQUIREMENTS IDENTIFIED BY AGENT")
print("=" * 70)

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


# --------------------------------------------------
# Show candidate results
# --------------------------------------------------

print("\n")
print("=" * 70)
print("FINAL RESUME SCREENING RESULTS")
print("=" * 70)

for candidate in results["candidates"]:

    print(
        f"\nRank {candidate['rank']}: "
        f"{candidate['name']}"
    )

    print(
        f"Overall Score: "
        f"{candidate['overall_score']:.2f}/100"
    )

    print(
        f"Semantic Score: "
        f"{candidate['semantic_score']:.2f}"
    )

    print(
        f"Skills Score: "
        f"{candidate['skill_score']:.2f}"
    )

    print(
        f"Experience Score: "
        f"{candidate['experience_score']:.2f}"
    )

    print(
        f"Education Score: "
        f"{candidate['education_score']:.2f}"
    )

    print(
        f"Recommendation: "
        f"{candidate['recommendation']}"
    )

    print("Strengths:")

    for skill in candidate["strengths"]:
        print(f"  ✓ {skill}")

    print("Skill Gaps:")

    if candidate["skill_gaps"]:

        for skill in candidate["skill_gaps"]:
            print(f"  ⚠ {skill}")

    else:

        print("  No major skill gaps identified.")