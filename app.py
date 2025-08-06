
from flask import Flask, request, jsonify, redirect
from forms import BookForm
from utils import load_books, save_books
import uuid


app = Flask(__name__)
app.secret_key = 'super_secret_key'


@app.route('/books', methods=['GET'])
def get_books():
    books = load_books()
    return jsonify(books), 200


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    books = load_books()
    book = next((b for b in books if str(b.get('id')) == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book), 200


@app.route('/books', methods=['POST'])
def add_book():
    form = BookForm(data=request.json)
    if form.validate():
        books = load_books()
        new_book = {
            'id': str(uuid.uuid4()),
            'title': form.title.data,
            'author': form.author.data,
            'year': form.year.data,
            'pages': form.pages.data,
            'description': form.description.data
        }
        books.append(new_book)
        save_books(books)
        return jsonify(new_book), 201

    return jsonify(form.errors), 400


@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    books = load_books()
    book = next((b for b in books if str(b.get('id')) == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    form = BookForm(data=request.json)
    if form.validate():
        book['title'] = form.title.data
        book['author'] = form.author.data
        book['year'] = form.year.data
        book['pages'] = form.pages.data
        book['description'] = form.description.data
        save_books(books)
        return jsonify(book), 200

    return jsonify(form.errors), 400


@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = load_books()
    updated_books = [b for b in books if str(b.get('id')) != book_id]
    if len(updated_books) == len(books):
        return jsonify({'error': 'Book not found'}), 404

    save_books(updated_books)
    return jsonify({'message': 'Book deleted'}), 200


@app.route('/')
def index():
    return redirect('/books')

if __name__ == '__main__':
    app.run(debug=True)