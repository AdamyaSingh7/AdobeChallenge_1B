# core/segment.py

from dataclasses import dataclass
from typing import List
from pathlib import Path
from .extractor import extract_outline
from .reader    import extract_pages

@dataclass
class Section:
    heading: str
    page:    int
    text:    str

def pdf_to_sections(pdf_path: str) -> List[Section]:
    outline = extract_outline(pdf_path)
    # fallback: one section at page 1 with the filename as heading
    if not outline:
        outline = [{"page": 1, "text": Path(pdf_path).stem}]

    pages = extract_pages(pdf_path)
    sections: List[Section] = []

    for idx, item in enumerate(outline):
        p = int(item["page"])
        # clamp
        p = max(1, min(p, len(pages)))

        # determine end page
        if idx + 1 < len(outline):
            nxt = int(outline[idx+1]["page"])
            end = max(1, min(nxt, len(pages)))
        else:
            end = len(pages) + 1

        chunk = "\n".join(pages[p-1 : end-1]).strip()
        if not chunk:
            chunk = pages[p-1].strip()

        sections.append(Section(
            heading=item["text"].strip(),
            page=p,
            text=chunk
        ))

    return sections
