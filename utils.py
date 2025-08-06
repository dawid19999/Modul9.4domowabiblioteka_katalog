

from pathlib import Path
import json

DATA_FILE = Path('books.json')

def load_books():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_books(books):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)