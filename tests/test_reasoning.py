from agent.parser import extract_resume_text
from agent.extractor import extract_resume_information
from agent.reasoning import CandidateReasoner


# --------------------------------------------------
# Load resume
# --------------------------------------------------

file_path = "data/resumes/candidate_01.txt"

resume_text = extract_resume_text(file_path)


# --------------------------------------------------
# Extract candidate information
# --------------------------------------------------

candidate = extract_resume_information(resume_text)


# --------------------------------------------------
# Job requirements
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
# Example score
# --------------------------------------------------

overall_score = 81.77


# --------------------------------------------------
# Generate reasoning
# --------------------------------------------------

reasoner = CandidateReasoner()

result = reasoner.generate_reasoning(
    candidate,
    overall_score,
    required_skills
)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("=" * 60)
print("AI SCREENING REASONING")
print("=" * 60)

print(f"\nCandidate: {result['candidate']}")

print(
    f"Overall Score: "
    f"{result['overall_score']:.2f}/100"
)

print(
    f"Recommendation: "
    f"{result['recommendation']}"
)

print("\nStrengths:")

for skill in result["strengths"]:
    print(f"✓ {skill}")


print("\nSkill Gaps:")

if result["skill_gaps"]:

    for skill in result["skill_gaps"]:
        print(f"⚠ {skill}")

else:
    print("No major skill gaps identified.")