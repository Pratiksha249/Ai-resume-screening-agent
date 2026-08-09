import re


KNOWN_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "Generative AI",
    "LLM",
    "Large Language Models",
    "Transformers",
    "PyTorch",
    "TensorFlow",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "OpenCV",
    "LangChain",
    "RAG",
    "Git",
    "Docker",
    "AWS",
    "Azure",
    "GCP",
]


class JobDescriptionAnalyzer:
    """
    Analyzes a job description and extracts
    important screening requirements.
    """

    def extract_required_skills(self, job_description):
        """
        Identify known technical skills mentioned
        in the job description.
        """

        found_skills = []

        text_lower = job_description.lower()

        for skill in KNOWN_SKILLS:

            if skill.lower() in text_lower:
                found_skills.append(skill)

        return found_skills

    def extract_minimum_experience(
        self,
        job_description
    ):
        """
        Extract minimum experience requirements
        expressed in years or months.
        """

        text = job_description.lower()

        year_matches = re.findall(
            r"(?:at least|minimum of|minimum)\s+"
            r"(\d+(?:\.\d+)?)\s*"
            r"(?:years?|yrs?)",
            text
        )

        month_matches = re.findall(
            r"(?:at least|minimum of|minimum)\s+"
            r"(\d+)\s*"
            r"(?:months?|mos?)",
            text
        )

        if year_matches:
            return float(year_matches[0]) * 12

        if month_matches:
            return float(month_matches[0])

        return 0.0

    def extract_education_keywords(
        self,
        job_description
    ):
        """
        Identify relevant educational fields
        mentioned in the job description.
        """

        education_keywords = [
            "Artificial Intelligence",
            "Machine Learning",
            "Computer Science",
            "Data Science",
            "Information Technology",
        ]

        found = []

        text_lower = job_description.lower()

        for keyword in education_keywords:

            if keyword.lower() in text_lower:
                found.append(keyword)

        return found

    def analyze(self, job_description):
        """
        Analyze the complete job description.
        """

        required_skills = (
            self.extract_required_skills(
                job_description
            )
        )

        minimum_experience = (
            self.extract_minimum_experience(
                job_description
            )
        )

        education_keywords = (
            self.extract_education_keywords(
                job_description
            )
        )

        return {
            "required_skills": required_skills,
            "minimum_experience_months":
                minimum_experience,
            "education_keywords":
                education_keywords
        }