import os
from typing import Dict, List

import numpy as np

from .extract_text import extract_text_from_pdf
from .preprocess import preprocess_text
from .embeddings import embed_text
from .similarity import compute_semantic_scores
from .keywords import compute_keyword_scores
from .ranking import combine_scores, build_resume_report


def load_job_description_pdf(file) -> str:
    raw_text = extract_text_from_pdf(file)
    clean_text = preprocess_text(raw_text)
    return clean_text


def load_resumes(files) -> Dict[str, str]:
    resumes: Dict[str, str] = {}
    for f in files:
        name = os.path.basename(f.name)
        raw = extract_text_from_pdf(f)
        clean = preprocess_text(raw)
        resumes[name] = clean
    return resumes


def embed_job_description(text: str):
    return embed_text(text)


def embed_resumes(resume_texts: Dict[str, str]) -> Dict[str, "np.ndarray"]:
    embeddings = {}
    for name, text in resume_texts.items():
        embeddings[name] = embed_text(text)
    return embeddings


def run_full_analysis(
    jd_text: str, resume_texts: Dict[str, str], skills_list: List[str]
):
    # 1. Embeddings
    job_emb = embed_job_description(jd_text)
    resume_embs = embed_resumes(resume_texts)

    # 2. Semantic similarity
    semantic_scores = compute_semantic_scores(job_emb, resume_embs)
    # semantic_scores: Dict[str, float]

    # 3. Keyword coverage
    jd_keywords, coverage_scores, found_keywords_all, missing_keywords_all = (
        compute_keyword_scores(jd_text, resume_texts, skills_list)
    )
    # coverage_scores: Dict[str, float]

    # 4. Combine scores
    combined = combine_scores(semantic_scores, coverage_scores)
    # combined: List[(name, final, sem, cov)]

    # 5. Build detailed reports
    final_reports = []
    for (name, final_score, sem, cov) in combined:
        rep = build_resume_report(
            resume_name=name,
            final_score=final_score,
            semantic_score=sem,
            coverage_score=cov,
            found_keywords=found_keywords_all.get(name, []),
            missing_keywords=missing_keywords_all.get(name, []),
        )
        final_reports.append(rep)

    return final_reports, jd_keywords
