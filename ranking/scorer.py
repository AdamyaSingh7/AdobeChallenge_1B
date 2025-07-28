# ranking/scorer.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise       import cosine_similarity
import numpy as np

BOOST_VERBS = {"create","send","convert","fill","sign"}
BOOST_VALUE = 0.1

def rank_sections(sections, persona, job, top_k=5):
    """
    sections: List[Section]
    persona/job: strings
    Returns top_k indices and similarity scores.
    """
    # 1) Build TF-IDF on section texts + query
    texts = [sec.text for sec in sections]
    query = f"{persona} needs to {job}"
    tfidf = TfidfVectorizer().fit(texts + [query])
    mat   = tfidf.transform(texts)
    qvec  = tfidf.transform([query])

    # 2) Compute cosine sims
    sims = cosine_similarity(mat, qvec).flatten()

    # 3) Verb-boost & length-penalty
    for i, sec in enumerate(sections):
        lw = len(sec.heading.split())
        if any(v in sec.heading.lower() for v in BOOST_VERBS):
            sims[i] += BOOST_VALUE
        sims[i] -= (lw / 1000)

    # 4) Pick top_k
    idxs = np.argsort(-sims)[:min(top_k, len(sims))].tolist()
    return idxs, sims[idxs].tolist()
