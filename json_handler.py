import json
from pathlib import Path

PROGRESS_FILE = Path("universities.json")

def save_progress(unis: dict) -> None:
    with PROGRESS_FILE.open("w", encoding="utf-8") as file:
        json.dump(unis, file, indent=4, ensure_ascii=False)

def load_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {}
    
    with PROGRESS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)
    
