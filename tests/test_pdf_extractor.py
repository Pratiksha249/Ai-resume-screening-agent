from agent.parser import extract_resume_text
from agent.extractor import extract_resume_information


# Path to your PDF
pdf_path = "data/resumes/test_resume.pdf"


# -----------------------------------------
# Step 1: Extract text from PDF
# -----------------------------------------

resume_text = extract_resume_text(
    pdf_path
)


print("=" * 70)
print("PDF → TEXT EXTRACTION")
print("=" * 70)

print(
    f"Extracted characters: {len(resume_text)}"
)


# -----------------------------------------
# Step 2: Extract candidate information
# -----------------------------------------

candidate = extract_resume_information(
    resume_text
)


# -----------------------------------------
# Step 3: Display extracted information
# -----------------------------------------

print("\n")
print("=" * 70)
print("EXTRACTED CANDIDATE INFORMATION")
print("=" * 70)


print("\nName:")
print(candidate["name"])


print("\nSkills:")
print(candidate["skills"])


print("\nEducation:")
print(candidate["education"])


print("\nExperience:")
print(candidate["experience"])


print("\nProjects:")

for project in candidate["projects"]:
    print(f"  • {project}")


print("\nResearch:")

print(candidate["research"])