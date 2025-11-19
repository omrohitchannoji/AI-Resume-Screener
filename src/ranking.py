from typing import List, Dict, Tuple

def combine_scores(
    semantic_scores: Dict[str, float],
    coverage_scores: Dict[str, float],
    alpha: float = 0.7,
) -> List[Tuple[str, float, float, float]]:
    """
    Combine semantic similarity with keyword coverage.
    final_score = alpha * semantic + (1 - alpha) * coverage

    Returns:
        List of tuples: (resume_name, final_score, semantic_score, coverage_score)
    """
    combined: List[Tuple[str, float, float, float]] = []

    for name, sem_score in semantic_scores.items():
        # sem_score MUST be a float
        cov_score = coverage_scores.get(name, 0.0)  # cov_score MUST be a float

        # Just to be super safe:
        sem_score = float(sem_score)
        cov_score = float(cov_score)

        final = alpha * sem_score + (1 - alpha) * cov_score

        combined.append((name, final, sem_score, cov_score))

    # Sort descending by final score
    combined.sort(key=lambda x: x[1], reverse=True)

    return combined


def build_resume_report(
    resume_name: str,
    final_score: float,
    semantic_score: float,
    coverage_score: float,
    found_keywords: List[str],
    missing_keywords: List[str],
) -> Dict:
    """
    Build an explainable report for a resume.
    This goes into Streamlit UI.
    """
    return {
        "name": resume_name,
        "final_score": round(final_score, 3),
        "semantic_similarity": round(semantic_score, 3),
        "keyword_coverage": round(coverage_score, 3),
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
    }
