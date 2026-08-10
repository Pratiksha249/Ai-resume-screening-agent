import re
from datetime import datetime


class CandidateScorer:
    """
    Calculates an overall candidate score using:

    - Semantic similarity
    - Required skills
    - Relevant experience
    - Education

    Default weights:
        Semantic     = 40%
        Skills       = 30%
        Experience   = 20%
        Education    = 10%
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

    # =========================================================
    # SKILL SCORE
    # =========================================================

    def calculate_skill_score(
        self,
        candidate_skills,
        required_skills
    ):
        """
        Calculate the percentage of required skills
        present in the candidate profile.
        """

        if not required_skills:
            return 0.0

        candidate_skills_lower = {
            skill.lower().strip()
            for skill in candidate_skills
        }

        required_skills_lower = {
            skill.lower().strip()
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

        return round(score * 100, 2)

    # =========================================================
    # EXPERIENCE SCORE
    # =========================================================

    def calculate_experience_score(
        self,
        experience_text,
        minimum_months
    ):
        """
        Calculate experience score using both:

        1. Explicit durations:
           - 8 months
           - 2 years

        2. Date ranges:
           - Feb 2026 - May 2026
           - Apr 2024 – Jun 2024
           - January 2023 - March 2024

        The final score is capped at 100.
        """

        if not experience_text:
            return 0.0

        text = experience_text.lower()

        total_months = 0.0

        # -----------------------------------------------------
        # 1. Explicit month durations
        # -----------------------------------------------------

        month_matches = re.findall(
            r"(\d+(?:\.\d+)?)\s*"
            r"(?:months?|mos?)",
            text
        )

        for months in month_matches:

            total_months += float(months)

        # -----------------------------------------------------
        # 2. Explicit year durations
        # -----------------------------------------------------

        year_matches = re.findall(
            r"(\d+(?:\.\d+)?)\s*"
            r"(?:years?|yrs?)",
            text
        )

        for years in year_matches:

            total_months += (
                float(years) * 12
            )

        # -----------------------------------------------------
        # 3. Date ranges
        #
        # Examples:
        #
        # Feb 2026 - May 2026
        # Apr 2024 – Jun 2024
        # January 2023 - March 2024
        # -----------------------------------------------------

        month_names = (
            "jan|feb|mar|apr|may|jun|jul|aug|sep|"
            "oct|nov|dec"
        )

        date_range_pattern = (
            rf"({month_names})[a-z]*\s+(\d{{4}})"
            rf"\s*[-–—]\s*"
            rf"({month_names})[a-z]*\s+(\d{{4}})"
        )

        date_ranges = re.findall(
            date_range_pattern,
            text
        )

        for (
            start_month,
            start_year,
            end_month,
            end_year
        ) in date_ranges:

            try:

                start_date = datetime.strptime(
                    f"{start_month[:3]} {start_year}",
                    "%b %Y"
                )

                end_date = datetime.strptime(
                    f"{end_month[:3]} {end_year}",
                    "%b %Y"
                )

                months = (
                    (end_date.year - start_date.year)
                    * 12
                    + (
                        end_date.month
                        - start_date.month
                    )
                    + 1
                )

                if months > 0:

                    total_months += months

            except ValueError:

                continue

        # -----------------------------------------------------
        # 4. No experience detected
        # -----------------------------------------------------

        if total_months <= 0:

            return 0.0

        # -----------------------------------------------------
        # 5. No minimum experience requirement
        # -----------------------------------------------------

        if minimum_months <= 0:

            return 100.0

        # -----------------------------------------------------
        # 6. Compare candidate experience with requirement
        # -----------------------------------------------------

        score = (
            total_months
            / minimum_months
        )

        # Cap score at 100
        score = min(score, 1.0) * 100

        return round(score, 2)

    # =========================================================
    # EDUCATION SCORE
    # =========================================================

    def calculate_education_score(
        self,
        education_text,
        required_keywords
    ):
        """
        Calculate education relevance based on
        keyword matching.
        """

        if not education_text:
            return 0.0

        if not required_keywords:
            return 100.0

        education_lower = (
            education_text.lower()
        )

        matched = 0

        for keyword in required_keywords:

            if keyword.lower() in education_lower:

                matched += 1

        score = (
            matched
            / len(required_keywords)
        ) * 100

        return round(score, 2)

    # =========================================================
    # OVERALL SCORE
    # =========================================================

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

            semantic_score
            * self.semantic_weight

            + skill_score
            * self.skills_weight

            + experience_score
            * self.experience_weight

            + education_score
            * self.education_weight
        )

        return round(
            overall_score,
            2
        )