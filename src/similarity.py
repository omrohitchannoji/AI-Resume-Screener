import numpy as np
from typing import Dict
from sklearn.metrics.pairwise import cosine_similarity

def compute_semantic_scores(
        job_embs:np.ndarray,
        resume_embs:Dict[str,np.ndarray]
) -> Dict[str,float]:
    
    scores={}
    
    job_vecs = job_embs.reshape(1,-1)

    for name,embs in resume_embs.items():
        res_vecs = embs.reshape(1,-1)

        sim = cosine_similarity(job_vecs,res_vecs)[0][0]

        scores[name] = float(sim)                       
    return scores
    
    