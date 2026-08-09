class CandidateRanker:
    """
    Ranks candidates based on their overall scores.
    """

    def rank_candidates(self, candidates):
        """
        Sort candidates from highest score to lowest score.
        """

        ranked_candidates = sorted(
            candidates,
            key=lambda candidate: candidate["overall_score"],
            reverse=True
        )

        for rank, candidate in enumerate(
            ranked_candidates,
            start=1
        ):
            candidate["rank"] = rank

        return ranked_candidates