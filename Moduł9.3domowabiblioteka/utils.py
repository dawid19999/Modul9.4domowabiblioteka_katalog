import json
import os

BOOKS_FILE = 'books.json'


def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_books(books):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as file:
        json.dump(books, file, indent=4, ensure_ascii=False)
