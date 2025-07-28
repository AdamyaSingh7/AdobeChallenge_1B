# ADOBE ROUND 1B

A robust, modular PDF intelligence tool that extracts and ranks the most relevant sections based on a given **persona** and **job-to-be-done**, supporting any document type or domain.

- **Document Agnostic**: Works with research papers, manuals, reports, etc.
- **Persona-Aware**: Tailors outputs to the user and their intent.
- **Lightweight & Offline**: No API or cloud dependency. Fully Dockerized.

---

## 🧠 Methodology

### 🔎 Methodology Overview

This pipeline is designed to be **generic**, **modular**, and **fast** (< 60 s for 10 PDFs) while producing **accurate** top‐K sections and summaries for *any* persona and job. We break the task into four main stages:

1. **Section Extraction (`core/extractor.py` + `core/segment.py`)**  
   - **TOC-First**: Uses embedded TOC if available via `doc.get_toc(simple=True)`.
   - **Font-Size Fallback**: Clusters font sizes to infer heading structure.
   - **Segmentation**: Forms `Section` objects with `heading`, `page`, and `text`.

2. **Ranking (`ranking/scorer.py`)**  
   - **TF-IDF Baseline**: Computes similarity between section text and query.
   - **Keyword Boosts & Penalties**: Domain heuristics via `utils/config.py`.
   - **2× or 3× Candidate Pool**: Expands candidate set, deduplicates, and selects top_k.

3. **Summarization (`ranking/summarizer.py`)**  
   - Uses **TextRank** to summarize top-ranked sections into ~7 meaningful lines.

4. **Orchestration & Output (`cli/run.py`)**  
   - Extracts → Ranks → Summarizes → Exports final JSON to `output/output.json`.
   - Docker-ready using `python:3.10-slim`.

---

## 🧰 Libraries & Tools Used

- `PyMuPDF` – PDF text + TOC extraction
- `scikit-learn` – TF-IDF, cosine similarity
- `networkx` – PageRank-based summarization
- Python 3.10, Docker

---

## 📋 Prerequisites

- **Docker** installed (version 20+)
- **Python** 3.8+ (only for local testing, not required for Docker)
- Dependencies in `requirements.txt`

---

## 🛠️ Installation (Local)
```bash
git clone https://github.com/AdamyaSingh7/AdobeChallenge_1B.git
cd AdobeChallenge_1B
```

---

## 🐳 Docker Setup

### 1. Build Image
### 🔧 Bash
```bash
docker build --platform linux/amd64 -t pdfintel:round1b .
```
### 🔧 powershell
```powershell
docker build --platform linux/amd64 -t pdfintel:round1b .
```
> ⚠️ **Note:** The build process takes approximately **1 to 1.5 minutes**, depending on your system.

### 2. Run
### 🔧 Bash
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  -e PERSONA="Travel Planner" \
  -e JOB="Plan a trip of 4 days for a group of 10 college friends." \
  pdfintel:round1b
```
### 🔧 powershell
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
