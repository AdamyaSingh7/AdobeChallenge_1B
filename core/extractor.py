# core/extractor.py
import fitz
from statistics import quantiles
from collections import Counter

def extract_outline(pdf_path: str) -> list[dict]:
    """
    Extract a list of {"page": int, "text": str} headings.
    1) Try embedded TOC (levels 1–2).
    2) Else fallback to rule-based font-size detection + title-case & length filter.
    """
    doc = fitz.open(pdf_path)

    # 1) TOC first
    toc = doc.get_toc(simple=True)  # [(level, title, page), …]
    if toc:
        outline = [
            {"page": page, "text": title.strip()}
            for level, title, page in toc
            if level <= 2 and title.strip()
        ]
        doc.close()
        return outline

    # 2) Fallback: gather spans
    spans = []
    for pnum, page in enumerate(doc, start=1):
        d = page.get_text("dict")
        for b in d["blocks"]:
            if b["type"] != 0: continue
            for ln in b["lines"]:
                txt = "".join(s["text"] for s in ln["spans"]).strip()
                if not txt: continue
                size = ln["spans"][0]["size"]
                spans.append((pnum, size, txt))
    doc.close()
    if not spans:
        return []

    # cluster font sizes into body vs headings
    sizes = [sz for _, sz, _ in spans]
    body = Counter(sizes).most_common(1)[0][0]
    uniq = sorted(set(sizes))
    higher = [s for s in uniq if s > body]
    thresh = higher[0] if higher else quantiles(sizes, n=100)[89]

    # filter & merge
    heads = []
    for p, sz, txt in spans:
        if sz < thresh: continue
        if heads and heads[-1]["page"]==p and abs(sz-heads[-1]["size"])<1:
            if txt not in heads[-1]["text"]:
                heads[-1]["text"] += " " + txt
        else:
            heads.append({"page":p, "size":sz, "text":txt})

    # strict filter: ≤ 12 words & ≥ 50% TitleCase tokens
    def is_heading(t:str) -> bool:
        w = t.split()
        if len(w)>12: return False
        cap = sum(1 for x in w if x and x[0].isupper())
        return (cap/len(w))>=0.5

    return [
        {"page":h["page"], "text":h["text"].strip()}
        for h in heads if is_heading(h["text"])
    ]
