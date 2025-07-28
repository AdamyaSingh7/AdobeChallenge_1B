# ADOBE ROUND 1B

A robust, modular PDF intelligence tool that extracts and ranks the most relevant sections based on a given **persona** and **job-to-be-done**, supporting any document type or domain.

- **Document Agnostic**: Works with research papers, manuals, reports, etc.
- **Persona-Aware**: Tailors outputs to the user and their intent.
- **Lightweight & Offline**: No API or cloud dependency. Fully Dockerized.

---

## Methodology

```markdown
# Methodology Overview

This pipeline is designed to be **generic**, **modular**, and **fast** (< 60 s for 10 PDFs) while producing **accurate** top‐K sections and summaries for *any* persona and job. We break the task into four main stages:

1. **Section Extraction (core/extractor.py + core/segment.py)**  
   - **TOC-First**: Most well-produced PDFs (manuals, reports, e-books) include an embedded Table of Contents. We call `doc.get_toc(simple=True)` via PyMuPDF and extract level 1–2 entries directly, preserving official titles and page numbers.  
   - **Font-Size Fallback**: If no TOC exists, we gather all text spans with their font sizes, identify the dominant “body” size via frequency, then select larger fonts as candidate headings. We merge nearby fragments on the same page, filter out runs longer than 12 words or with fewer than 50 % title-case tokens, and emit the remaining as headings.  
   - **Segmentation**: With a structured list of `(page, text)` headings, we slice the PDF’s full-page text (extracted via `page.get_text("text")`) between headings to produce `Section` objects containing `heading`, `page`, and `text`. Empty slices fall back to the raw page text to guarantee non-empty content.

2. **Ranking (ranking/scorer.py)**  
   - **TF-IDF Baseline**: We vectorize all section texts and the concatenated query (`"{persona} needs to {job}"}`) using `TfidfVectorizer`. Cosine similarity provides a strong general signal of relevance across domains.  
   - **Keyword Boosts & Penalties**: Recognizing that certain headings (e.g. “Things to Do”, “Restaurants”, “Hotels”) are pivotal for trip planning, we apply configurable boosts when those keywords appear. Likewise, we lightly penalize off-target sections (e.g. “History”, “Culture”) for planning tasks. This simple heuristic layer can be adapted per domain by editing `utils/config.py` rather than core code.  
   - **2× or 3× Candidate Pool**: We initially score `top_k × 3` sections, then **deduplicate** by `(document, page)` to avoid redundant picks, and finally select the first unique `top_k`.

3. **Summarization (ranking/summarizer.py)**  
   - We apply a **TextRank** algorithm on the sentences of each selected section’s text. After splitting into up to 40 sentences, we compute pairwise TF-IDF similarities, build a graph, run PageRank, and select the top 7 sentences (ordered as in the source). This yields concise yet contextual summaries.

4. **Orchestration & Output (cli/run.py)**  
   - The CLI ties everything together: it loads PDFs, runs the extractor, computes headings and slices, ranks and deduplicates, summarizes, and dumps a single `output.json` per the expected schema.  
   - **Docker-Ready**: A lightweight `python:3.10-slim` image with only PyMuPDF, scikit-learn, and networkx ensures offline execution under 1 GB.

By cleanly separating PDF I/O, extraction, ranking, and summarization into distinct modules—and centralizing any domain-specific heuristics in a single `config.py`—this solution generalizes effortlessly to new document sets (research papers, textbooks, financial reports) and new personas/jobs, while staying maintainable and performant.

---

## 🧰 Libraries & Tools Used

- `PyMuPDF` – PDF text + TOC extraction
- `scikit-learn` – TF-IDF, cosine similarity
- `networkx` – PageRank-based summarization
- Python 3.10, Docker

---

## Prerequisites

- **Docker** installed (version 20+).
- **Python** 3.8 or later (for local testing).
- Python dependencies listed in `requirements.txt`

## 🐳 Docker Setup

### 1. Build Image

```bash
docker build --platform linux/amd64 -t pdfintel:round1b .
```
```powershell
docker build --platform linux/amd64 -t pdfintel:round1b .
```

### 2. Run

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  -e PERSONA="Travel Planner" \
  -e JOB="Plan a trip of 4 days for a group of 10 college friends." \
  pdfintel:round1b
```
```powershell
docker run --rm `
  -v ${PWD}\input:/app/input `
  -v ${PWD}\output:/app/output `
  --network none `
  -e PERSONA="Travel Planner" `
  -e JOB="Plan a trip of 4 days for a group of 10 college friends." `
  pdfintel:round1b
```

> Replace persona + job as needed. Input should be PDF files inside the `input/` folder.

---

## 📦 [Sample Output](output/output.json)

---

## 📎 Deliverables

- ✅ `README.md` (this file)
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `output/output.json`