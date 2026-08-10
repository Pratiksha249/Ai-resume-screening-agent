from agent.parser import extract_resume_text
from agent.extractor import extract_resume_information


def test_resume_skills_extraction():

    resume_path = "data/resumes/test_resume.pdf"

    text = extract_resume_text(
        resume_path
    )

    candidate = extract_resume_information(
        text
    )

    skills = candidate["skills"]

    # Basic skills that should definitely
    # be detected from the test resume.
    assert "Python" in skills
    assert "Machine Learning" in skills
    assert "Deep Learning" in skills
    assert "Artificial Intelligence" in skills
    assert "Generative AI" in skills


def test_nlp_inference():

    resume_path = "data/resumes/test_resume.pdf"

    text = extract_resume_text(
        resume_path
    )

    candidate = extract_resume_information(
        text
    )

    skills = candidate["skills"]

    # The test resume contains multiple
    # strong NLP indicators such as:
    # LLM, Transformers, RAG, NLTK, spaCy.
    assert "NLP" in skills