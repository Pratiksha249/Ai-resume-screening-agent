from pathlib import Path

from agent.parser import extract_resume_text
from agent.extractor import extract_resume_information
from agent.embeddings import EmbeddingMatcher
from agent.scorer import CandidateScorer
from agent.ranker import CandidateRanker
from agent.reasoning import CandidateReasoner
from agent.jd_analyzer import JobDescriptionAnalyzer


class ResumeScreeningAgent:
    """
    Main orchestration class for the resume screening system.

    It coordinates:
    1. Resume parsing
    2. Information extraction
    3. Semantic matching
    4. Candidate scoring
    5. Candidate ranking
    6. Screening reasoning
    """

    def __init__(self):

        self.matcher = EmbeddingMatcher()
        self.scorer = CandidateScorer()
        self.ranker = CandidateRanker()
        self.reasoner = CandidateReasoner()
        self.jd_analyzer = JobDescriptionAnalyzer()

    # =========================================================
    # PROCESS ONE RESUME
    # =========================================================

    def process_resume(
        self,
        resume_path,
        job_description,
        required_skills,
        minimum_months=6
    ):
        """
        Process one resume from file to final screening result.
        """

        # -----------------------------------------
        # 1. Extract resume text
        # -----------------------------------------

        resume_text = extract_resume_text(
            resume_path
        )

        # -----------------------------------------
        # 2. Extract structured information
        # -----------------------------------------

        candidate = extract_resume_information(
            resume_text
        )

        # -----------------------------------------
        # 3. Calculate semantic similarity
        # -----------------------------------------

        similarity = self.matcher.calculate_similarity(
            job_description,
            resume_text
        )

        semantic_score = similarity * 100

        # -----------------------------------------
        # 4. Calculate skill score
        # -----------------------------------------

        skill_score = self.scorer.calculate_skill_score(
            candidate["skills"],
            required_skills
        )

        # -----------------------------------------
        # 5. Calculate experience score
        # -----------------------------------------
        #
        # The scorer now considers:
        # - Experience duration
        # - Experience relevance to required skills
        #
        # required_skills is passed into the scorer
        # so that experience relevance can be calculated.
        # -----------------------------------------

        experience_score = (
            self.scorer.calculate_experience_score(
                candidate["experience"],
                minimum_months,
                required_skills
            )
        )

        # -----------------------------------------
        # 6. Calculate education score
        # -----------------------------------------

        education_score = (
            self.scorer.calculate_education_score(
                candidate["education"],
                [
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Computer Science"
                ]
            )
        )

        # -----------------------------------------
        # 7. Calculate overall score
        # -----------------------------------------

        overall_score = (
            self.scorer.calculate_overall_score(
                semantic_score,
                skill_score,
                experience_score,
                education_score
            )
        )

        # -----------------------------------------
        # 8. Generate reasoning
        # -----------------------------------------

        reasoning = self.reasoner.generate_reasoning(
            candidate,
            overall_score,
            required_skills
        )

        # -----------------------------------------
        # 9. Return complete result
        # -----------------------------------------

        return {
            "name": candidate["name"],

            "resume_path": str(
                resume_path
            ),

            "skills": candidate["skills"],

            "education": candidate["education"],

            "experience": candidate["experience"],

            "projects": candidate["projects"],

            "research": candidate["research"],

            "semantic_score": round(
                semantic_score,
                2
            ),

            "skill_score": round(
                skill_score,
                2
            ),

            "experience_score": round(
                experience_score,
                2
            ),

            "education_score": round(
                education_score,
                2
            ),

            "overall_score": overall_score,

            "recommendation": reasoning[
                "recommendation"
            ],

            "strengths": reasoning[
                "strengths"
            ],

            "skill_gaps": reasoning[
                "skill_gaps"
            ]
        }

    # =========================================================
    # SCREEN ALL CANDIDATES
    # =========================================================

    def screen_candidates(
        self,
        resume_folder,
        job_description
    ):
        """
        Analyze the job description and screen
        all supported resumes in the folder.
        """

        # -----------------------------------------
        # 1. Analyze the job description
        # -----------------------------------------

        requirements = self.jd_analyzer.analyze(
            job_description
        )

        required_skills = requirements[
            "required_skills"
        ]

        minimum_months = requirements[
            "minimum_experience_months"
        ]

        # -----------------------------------------
        # 2. Find resumes
        # -----------------------------------------

        resume_folder = Path(
            resume_folder
        )

        candidates = []

        supported_extensions = {
            ".pdf",
            ".docx",
            ".txt"
        }

        # -----------------------------------------
        # 3. Process each resume
        # -----------------------------------------

        for resume_path in resume_folder.iterdir():

            if (
                resume_path.suffix.lower()
                not in supported_extensions
            ):
                continue

            print(
                f"Processing: "
                f"{resume_path.name}"
            )

            try:

                result = self.process_resume(
                    resume_path,
                    job_description,
                    required_skills,
                    minimum_months
                )

                candidates.append(
                    result
                )

            except Exception as error:

                print(
                    f"Error processing "
                    f"{resume_path.name}: "
                    f"{error}"
                )

        # -----------------------------------------
        # 4. Rank candidates
        # -----------------------------------------

        ranked_candidates = (
            self.ranker.rank_candidates(
                candidates
            )
        )

        # -----------------------------------------
        # 5. Return final results
        # -----------------------------------------

        return {
            "requirements": requirements,

            "candidates": ranked_candidates
        }