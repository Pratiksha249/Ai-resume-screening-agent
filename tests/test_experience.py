from agent.scorer import CandidateScorer


def test_experience_duration_months():

    scorer = CandidateScorer()

    experience = "AI Research Intern - 8 months"

    months = scorer.calculate_experience_duration(
        experience
    )

    assert months == 8


def test_experience_duration_years():

    scorer = CandidateScorer()

    experience = "Software Developer - 2 years"

    months = scorer.calculate_experience_duration(
        experience
    )

    assert months == 24


def test_experience_score_meets_requirement():

    scorer = CandidateScorer()

    experience = "AI Research Intern - 8 months"

    score = scorer.calculate_experience_score(
        experience,
        6,
        [
            "Python",
            "Machine Learning",
            "Artificial Intelligence"
        ]
    )

    assert score > 0
    assert score <= 100