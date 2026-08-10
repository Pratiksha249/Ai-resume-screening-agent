from agent.parser import extract_resume_text


pdf_path = "data/resumes/test_resume.pdf"


text = extract_resume_text(pdf_path)


print("=" * 70)
print("PDF TEXT EXTRACTION TEST")
print("=" * 70)

print("\nExtracted characters:", len(text))

print("\nFirst 2000 characters:")
print("-" * 70)

print(text[:2000])