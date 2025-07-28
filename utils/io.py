# utils/io.py
import json
from datetime import datetime
import pathlib

def dump_json(obj: dict, out_path: pathlib.Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

def timestamp() -> str:
    return datetime.now().astimezone().isoformat()
