from keybert import KeyBERT
from typing import List, Dict, Tuple
import re

kw_model = KeyBERT(model="all-MiniLM-L6-v2")


def extract_keywords_keybert(text: str, top_n: int = 20) -> List[str]:
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        top_n=top_n,
    )
    return [kw for kw, score in keywords]


def extract_skills_custom(text: str, skills_list: List[str]) -> List[str]:
    text_lower = text.lower()
    found = []
    for skill in skills_list:
        if skill.lower() in text_lower:
            found.append(skill)
    return list(set(found))


def keyword_coverage(required: List[str], found: List[str]) -> float:
    if not required:
        return 1.0
    req_set = set([r.lower() for r in required])
    found_set = set([f.lower() for f in found])

    overlap = found_set.intersection(req_set)
    return len(overlap) / len(req_set)


def missing_keywords(required: List[str], found: List[str]) -> List[str]:
    req_set = set([r.lower() for r in required])
    found_set = set([f.lower() for f in found])
    missing = req_set - found_set
    return list(missing)


def compute_keyword_scores(
    jd_text: str, resume_texts: Dict[str, str], skills_list: List[str]
):
    """
    Returns:
      jd_keywords: List[str]
      coverage_scores: Dict[str, float]
      found_keywords_all: Dict[str, List[str]]
      missing_keywords_all: Dict[str, List[str]]
    """
    jd_keywords = extract_keywords_keybert(jd_text)

    coverage_scores: Dict[str, float] = {}
    found_keywords_all: Dict[str, List[str]] = {}
    missing_keywords_all: Dict[str, List[str]] = {}

    for name, text in resume_texts.items():
        found = extract_skills_custom(text, skills_list)
        missing = missing_keywords(jd_keywords, found)
        coverage = keyword_coverage(jd_keywords, found)

        coverage_scores[name] = float(coverage)  # float
        found_keywords_all[name] = found        # list[str]
        missing_keywords_all[name] = missing    # list[str]

    return jd_keywords, coverage_scores, found_keywords_all, missing_keywords_all
