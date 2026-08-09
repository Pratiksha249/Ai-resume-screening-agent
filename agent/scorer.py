class CandidateScorer:
    """
    Calculates an overall candidate score using
    semantic similarity, skills, experience,
    and education.
    """

    def __init__(
        self,
        semantic_weight=0.40,
        skills_weight=0.30,
        experience_weight=0.20,
        education_weight=0.10
    ):

        self.semantic_weight = semantic_weight
        self.skills_weight = skills_weight
        self.experience_weight = experience_weight
        self.education_weight = education_weight

    def calculate_skill_score(
        self,
        candidate_skills,
        required_skills
    ):
        """
        Calculate how many required skills
        are present in the candidate profile.
        """

        if not required_skills:
            return 0.0

        candidate_skills_lower = {
            skill.lower()
            for skill in candidate_skills
        }

        required_skills_lower = {
            skill.lower()
            for skill in required_skills
        }

        matched_skills = (
            candidate_skills_lower
            & required_skills_lower
        )

        score = (
            len(matched_skills)
            / len(required_skills_lower)
        )

        return score * 100

    def calculate_experience_score(
        self,
        experience_text,
        minimum_months
    ):
        """
        Estimate experience score based on
        the number of months mentioned in the resume.
        """

        if not experience_text:
            return 0.0

        text = experience_text.lower()

        total_months = 0

        import re

        month_matches = re.findall(
            r"(\d+)\s*(?:months?|mos?)",
            text
        )

        year_matches = re.findall(
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            text
        )

        for months in month_matches:
            total_months += int(months)

        for years in year_matches:
            total_months += float(years) * 12

        if minimum_months <= 0:
            return 100.0

        score = total_months / minimum_months

        return min(score, 1.0) * 100

    def calculate_education_score(
        self,
        education_text,
        required_keywords
    ):
        """
        Calculate education relevance using
        keyword matching.
        """

        if not education_text:
            return 0.0

        education_lower = education_text.lower()

        matched = 0

        for keyword in required_keywords:

            if keyword.lower() in education_lower:
                matched += 1

        if not required_keywords:
            return 100.0

        return (
            matched / len(required_keywords)
        ) * 100

    def calculate_overall_score(
        self,
        semantic_score,
        skill_score,
        experience_score,
        education_score
    ):
        """
        Combine all individual scores into
        one overall score out of 100.
        """

        overall_score = (
            semantic_score * self.semantic_weight
            + skill_score * self.skills_weight
            + experience_score * self.experience_weight
            + education_score * self.education_weight
        )

        return round(overall_score, 2)