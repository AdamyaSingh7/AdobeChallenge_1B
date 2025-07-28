# ranking/summarizer.py

import re
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

def textrank_summary(text: str, max_sents: int = 7) -> str:
    # 1) Clean and split into sentences
    txt = text.replace("\n", " ").strip()
    sents = re.split(r'(?<=[\.!?])\s+', txt)
    sents = [s for s in sents if s]
    if not sents:
        return ""

    # If fewer than max_sents, just join them all
    if len(sents) <= max_sents:
        return " ".join(sents)

    # 2) Build TF-IDF matrix and similarity graph
    tfidf = TfidfVectorizer().fit_transform(sents).toarray()
    sim   = tfidf @ tfidf.T
    G     = nx.from_numpy_array(sim)

    # 3) Run PageRank
    pr = nx.pagerank(G, weight=None)

    # 4) Pick top-scoring sentences
    top_items = sorted(pr.items(), key=lambda x: -x[1])[:max_sents]
    top_idxs  = sorted([idx for idx, _ in top_items])

    # 5) Return them in original order
    return " ".join(sents[i] for i in top_idxs)
