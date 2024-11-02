from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Data buku (database sederhana)
books = [
    {
        "id": 1,
        "title": "Laskar Pelangi",
        "author": "Andrea Hirata",
        "year": 2005,
        "genre": "Drama"
    },
    {
        "id": 2,
        "title": "Bumi Manusia",
        "author": "Pramoedya Ananta Toer",
        "year": 1980,
        "genre": "Historical Fiction"
    }
]

# Helper functions
def get_all_books():
    return books

def get_book_by_id(book_id):
    return next((book for book in books if book["id"] == book_id), None)

# Resource untuk daftar buku (GET & POST)
class BookList(Resource):
    def get(self):
        return jsonify(get_all_books())

    def post(self):
        new_book = request.get_json()
        new_book["id"] = books[-1]["id"] + 1 if books else 1
        books.append(new_book)
        return jsonify(new_book), 201

# Resource untuk buku individu (GET, PUT, DELETE)
class Book(Resource):
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if book:
            return jsonify(book)
        return jsonify({"error": "Book not found"}), 404

    def put(self, book_id):
        book = get_book_by_id(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        update_data = request.get_json()
        book.update(update_data)
        return jsonify(book)

    def delete(self, book_id):
        global books
        books = [book for book in books if book["id"] != book_id]
        return jsonify({"message": "Book deleted"}), 204

# Menambahkan endpoint ke API
api.add_resource(BookList, "/books")
api.add_resource(Book, "/books/<int:book_id>")

# Menjalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
