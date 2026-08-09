from agent.parser import extract_resume_text
from agent.extractor import extract_resume_information


file_path = "data/resumes/candidate_01.txt"


# Step 1: Read the resume
resume_text = extract_resume_text(file_path)


# Step 2: Extract structured information
candidate = extract_resume_information(resume_text)


print("=" * 60)
print("EXTRACTED CANDIDATE INFORMATION")
print("=" * 60)

print("\nName:")
print(candidate["name"])

print("\nSkills:")
print(candidate["skills"])

print("\nEducation:")
print(candidate["education"])

print("\nExperience:")
print(candidate["experience"])

print("\nProjects:")
print(candidate["projects"])

print("\nResearch:")
print(candidate["research"])