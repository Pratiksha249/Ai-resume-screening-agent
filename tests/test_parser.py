from agent.parser import extract_resume_text


def test_resume_text_extraction():

    resume_path = "data/resumes/test_resume.pdf"

    text = extract_resume_text(
        resume_path
    )

    assert text
    assert len(text) > 100


def test_resume_contains_candidate_name():

    resume_path = "data/resumes/test_resume.pdf"

    text = extract_resume_text(
        resume_path
    )

    assert "PRATIKSHA" in text.upper()