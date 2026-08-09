import csv
from pathlib import Path


class ResultsExporter:
    """
    Exports resume screening results into
    CSV format.
    """

    def export_csv(
        self,
        candidates,
        output_path="outputs/screening_results.csv"
    ):
        """
        Save screening results as a CSV file.
        """

        output_path = Path(output_path)

        # Create output directory if it doesn't exist
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        fieldnames = [
            "rank",
            "candidate",
            "overall_score",
            "recommendation",
            "semantic_score",
            "skill_score",
            "experience_score",
            "education_score",
            "matched_skills",
            "skill_gaps"
        ]

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for candidate in candidates:

                writer.writerow({
                    "rank": candidate["rank"],
                    "candidate": candidate["name"],
                    "overall_score":
                        candidate["overall_score"],
                    "recommendation":
                        candidate["recommendation"],
                    "semantic_score":
                        candidate["semantic_score"],
                    "skill_score":
                        candidate["skill_score"],
                    "experience_score":
                        candidate["experience_score"],
                    "education_score":
                        candidate["education_score"],
                    "matched_skills":
                        ", ".join(
                            candidate["strengths"]
                        ),
                    "skill_gaps":
                        ", ".join(
                            candidate["skill_gaps"]
                        )
                })

        return output_path