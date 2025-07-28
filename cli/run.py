# cli/run.py

import argparse
import os
import pathlib

from core.segment       import pdf_to_sections
from ranking.scorer     import rank_sections
from ranking.summarizer import textrank_summary
from utils.io           import dump_json, timestamp

def process_collection(input_dir: str,
                       output_dir: str,
                       persona: str,
                       job: str,
                       top_k: int = 5):
    # 1) Gather all sections
    pdf_paths = sorted(pathlib.Path(input_dir).glob("*.pdf"))
    all_secs, sec_docs = [], []
    for pdf in pdf_paths:
        secs = pdf_to_sections(str(pdf))
        all_secs.extend(secs)
        sec_docs.extend([pdf.name] * len(secs))

    # 2) Rank more than needed, so we can de-duplicate
    idxs, scores = rank_sections(all_secs, persona, job, top_k * 3)

    # 3) De-duplicate by (document, page), keep first top_k
    unique_idxs = []
    seen = set()
    for idx in idxs:
        sec = all_secs[idx]
        doc = sec_docs[idx]
        key = (doc, sec.page)
        if key not in seen:
            seen.add(key)
            unique_idxs.append(idx)
        if len(unique_idxs) >= top_k:
            break
    idxs = unique_idxs

    # 4) Build output lists
    extracted = []
    subanalysis = []
    for rank, idx in enumerate(idxs, start=1):
        sec = all_secs[idx]
        doc = sec_docs[idx]

        extracted.append({
            "document":        doc,
            "section_title":   sec.heading,
            "importance_rank": rank,
            "page_number":     sec.page
        })
        subanalysis.append({
            "document":     doc,
            "refined_text": textrank_summary(sec.text),
            "page_number":  sec.page
        })

    # 5) Final JSON
    output = {
        "metadata": {
            "input_documents":      [p.name for p in pdf_paths],
            "persona":              persona,
            "job_to_be_done":       job,
            "processing_timestamp": timestamp()
        },
        "extracted_sections":    extracted,
        "subsection_analysis":   subanalysis
    }

    out_path = pathlib.Path(output_dir) / "output.json"
    dump_json(output, out_path)
    print(f"✅ Wrote output to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",  required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--persona",    required=True)
    parser.add_argument("--job",        required=True)
    parser.add_argument("--top_k",      type=int, default=5)
    args = parser.parse_args()

    # If Docker placeholders are literal, substitute env vars
    if args.persona.startswith("${") and "PERSONA" in os.environ:
        args.persona = os.environ["PERSONA"]
    if args.job.startswith("${") and "JOB" in os.environ:
        args.job = os.environ["JOB"]

    process_collection(**vars(args))
