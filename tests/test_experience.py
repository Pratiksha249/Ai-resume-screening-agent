from agent.parser import extract_resume_text
from agent.extractor import extract_resume_information
from agent.scorer import CandidateScorer


files = [
    "data/resumes/candidate_01.txt",
    "data/resumes/candidate_02.txt",
    "data/resumes/candidate_03.txt",
    "data/resumes/candidate_04.txt",
]


scorer = CandidateScorer()

minimum_months = 6


for file_path in files:

    print("\n" + "=" * 70)
    print(file_path)
    print("=" * 70)

    # Extract raw text
    text = extract_resume_text(file_path)

    # Extract structured information
    candidate = extract_resume_information(text)

    print("\nCandidate:")
    print(candidate["name"])

    print("\nExperience extracted:")
    print(candidate["experience"])

    # Calculate experience score
    score = scorer.calculate_experience_score(
        candidate["experience"],
        minimum_months
    )

    print("\nExperience score:")
    print(score)