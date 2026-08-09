from agent.ranker import CandidateRanker


candidates = [
    {
        "name": "Ananya Sharma",
        "overall_score": 81.77
    },
    {
        "name": "Rahul Mehta",
        "overall_score": 74.32
    },
    {
        "name": "Priya Nair",
        "overall_score": 91.20
    },
    {
        "name": "Arjun Kumar",
        "overall_score": 68.45
    }
]


ranker = CandidateRanker()

ranked_candidates = ranker.rank_candidates(
    candidates
)


print("=" * 60)
print("CANDIDATE RANKING")
print("=" * 60)

for candidate in ranked_candidates:

    print(
        f"Rank {candidate['rank']}: "
        f"{candidate['name']} "
        f"→ {candidate['overall_score']:.2f}/100"
    )