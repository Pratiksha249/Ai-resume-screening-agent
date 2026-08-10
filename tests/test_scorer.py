from agent.scorer import CandidateScorer


def test_skill_score():

    scorer = CandidateScorer()

    candidate_skills = [
        "Python",
        "Machine Learning",
        "Deep Learning"
    ]

    required_skills = [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP"
    ]

    score = scorer.calculate_skill_score(
        candidate_skills,
        required_skills
    )

    assert score == 75.0


def test_education_score():

    scorer = CandidateScorer()

    education = (
        "MSc Artificial Intelligence "
        "and Machine Learning"
    )

    required_keywords = [
        "Artificial Intelligence",
        "Machine Learning",
        "Computer Science"
    ]

    score = scorer.calculate_education_score(
        education,
        required_keywords
    )

    assert score == 66.67


def test_overall_score():

    scorer = CandidateScorer()

    score = scorer.calculate_overall_score(
        semantic_score=80,
        skill_score=90,
        experience_score=100,
        education_score=80
    )

    assert score == 87.0