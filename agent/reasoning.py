class CandidateReasoner:
    """
    Generates an explanation for a candidate's
    screening result.
    """

    def generate_recommendation(self, overall_score):
        """
        Convert the overall score into a recommendation.
        """

        if overall_score >= 85:
            return "Strong Match"

        elif overall_score >= 70:
            return "Good Match"

        elif overall_score >= 55:
            return "Moderate Match"

        else:
            return "Low Match"

    def identify_strengths(
        self,
        candidate,
        required_skills
    ):
        """
        Identify skills from the candidate that
        match the job requirements.
        """

        candidate_skills = {
            skill.lower()
            for skill in candidate["skills"]
        }

        required_skills_lower = {
            skill.lower()
            for skill in required_skills
        }

        matched_skills = (
            candidate_skills
            & required_skills_lower
        )

        return sorted(matched_skills)

    def identify_skill_gaps(
        self,
        candidate,
        required_skills
    ):
        """
        Identify required skills missing from
        the candidate's resume.
        """

        candidate_skills = {
            skill.lower()
            for skill in candidate["skills"]
        }

        required_skills_lower = {
            skill.lower()
            for skill in required_skills
        }

        missing_skills = (
            required_skills_lower
            - candidate_skills
        )

        return sorted(missing_skills)

    def generate_reasoning(
        self,
        candidate,
        overall_score,
        required_skills
    ):
        """
        Generate a structured screening explanation.
        """

        recommendation = self.generate_recommendation(
            overall_score
        )

        strengths = self.identify_strengths(
            candidate,
            required_skills
        )

        skill_gaps = self.identify_skill_gaps(
            candidate,
            required_skills
        )

        return {
            "candidate": candidate["name"],
            "overall_score": overall_score,
            "recommendation": recommendation,
            "strengths": strengths,
            "skill_gaps": skill_gaps
        }