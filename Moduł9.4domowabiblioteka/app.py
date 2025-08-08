
from flask import Flask, render_template, redirect, url_for, request, jsonify
from forms import BookForm
from utils import load_books, save_books
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'


@app.route('/')
def index():
    books = load_books()
    form = BookForm()
    return render_template('index.html', books=books, form=form)


@app.route('/add', methods=['POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        books = load_books()
        new_book = {
            'id': str(uuid.uuid4()),
            'title': form.title.data,
            'author': form.author.data,
            'year': form.year.data,
            'description': form.description.data,
            'pages': form.pages.data
        }
        books.append(new_book)
        save_books(books)
        return redirect(url_for('index'))
    books = load_books()
    return render_template('index.html', books=books, form=form)


@app.route('/delete/<book_id>', methods=['POST'])
def delete_book(book_id):
    books = load_books()
    books = [b for b in books if b['id'] != book_id]
    save_books(books)
    return redirect(url_for('index'))


# ----------------------
#        REST API
# ----------------------

@app.route('/api/books', methods=['GET'])
def api_get_books():
    books = load_books()
    return jsonify(books), 200


@app.route('/api/books/<book_id>', methods=['GET'])
def api_get_single_book(book_id):
    books = load_books()
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404


@app.route('/api/books', methods=['POST'])
def api_add_book():
    data = request.json
    form = BookForm(data=data)
    if form.validate():
        books = load_books()
        new_book = {
            'id': str(uuid.uuid4()),
            'title': form.title.data,
            'author': form.author.data,
            'year': form.year.data,
            'description': form.description.data,
            'pages': form.pages.data
        }
        books.append(new_book)
        save_books(books)
        return jsonify(new_book), 201
    return jsonify(form.errors), 400


@app.route('/api/books/<book_id>', methods=['PUT'])
def api_update_book(book_id):
    data = request.json
    form = BookForm(data=data)
    if not form.validate():
        return jsonify(form.errors), 400

    books = load_books()
    for book in books:
        if book['id'] == book_id:
            book.update({
                'title': form.title.data,
                'author': form.author.data,
                'year': form.year.data,
                'description': form.description.data,
                'pages': form.pages.data
            })
            save_books(books)
            return jsonify(book), 200

    return jsonify({'error': 'Book not found'}), 404


@app.route('/api/books/<book_id>', methods=['DELETE'])
def api_delete_book(book_id):
    books = load_books()
    updated_books = [b for b in books if b['id'] != book_id]
    if len(updated_books) == len(books):
        return jsonify({'error': 'Book not found'}), 404
    save_books(updated_books)
    return jsonify({'message': 'Book deleted'}), 200


@app.route('/api/books/search', methods=['GET'])
def api_search_books():
    query = request.args.get('q', '').lower()
    books = load_books()
    filtered = [
        book for book in books
        if query in book['title'].lower() or query in book['author'].lower()
    ]
    return jsonify(filtered), 200


@app.route('/api/books/sort', methods=['GET'])
def api_sort_books():
    sort_by = request.args.get('sort_by', 'title')
    valid_fields = ['title', 'author', 'year', 'pages']
    if sort_by not in valid_fields:
        return jsonify({'error': f'Invalid sort field. Use one of {valid_fields}'}), 400

    books = load_books()
    sorted_books = sorted(books, key=lambda b: str(b.get(sort_by, '')).lower())
    return jsonify(sorted_books), 200


@app.route('/api/books/stats', methods=['GET'])
def api_books_stats():
    books = load_books()
    total = len(books)
    total_pages = sum(book.get('pages', 0) for book in books)
    avg_pages = round(total_pages / total, 2) if total > 0 else 0
    return jsonify({
        'total_books': total,
        'total_pages': total_pages,
        'avg_pages': avg_pages
    }), 200


if __name__ == '__main__':
    app.run(debug=True)