from agent.parser import extract_resume_text


file_path = "data/resumes/candidate_01.txt"

text = extract_resume_text(file_path)

print("=" * 60)
print("EXTRACTED RESUME")
print("=" * 60)

print(text)