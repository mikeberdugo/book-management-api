import pytest
from fastapi.testclient import TestClient
from app.main import app  # Cambia a la ruta de tu aplicación FastAPI

client = TestClient(app)

# Prueba para crear un libro
def test_create_book():
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "isbn": "978074327355"
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    assert response.json()["author"] == book_data["author"]

# Prueba para obtener todos los libros
def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Prueba para buscar libros por título
def test_search_books_by_title():
    response = client.get("/books/The Great Gatsby")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Esperamos que haya al menos un libro

# Prueba para buscar libros con un término que no existe
def test_search_books_by_title_not_found():
    response = client.get("/books/Nonexistent Book")
    assert response.status_code == 200
    assert len(response.json()) == 0  # No debería haber libros con este título

# Prueba para eliminar un libro
def test_delete_book():
    # Primero, creamos un libro
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "isbn": "978045152493"
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    
    # Ahora, lo eliminamos
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

    # Verificamos que el libro fue eliminado
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404

# Prueba para actualizar un libro
def test_update_book():
    # Primero, creamos un libro
    book_data = {
        "title": "Moby Dick",
        "author": "Herman Melville",
        "year": 1851,
        "isbn": "978014243724"
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]
    
    # Actualizamos el libro
    updated_data = {
        "title": "Moby Dick (Updated)",
        "author": "Herman Melville",
        "year": 1851,
        "isbn": "978014243724"
    }
    response = client.put(f"/books/{book_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]

# Prueba para obtener libros con filtros (por autor o año)
def test_get_books_filtered():
    # Filtrar por autor
    response = client.get("/books/?author=George Orwell")
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    # Filtrar por año
    response = client.get("/books/?year=1925")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Prueba de búsqueda combinada (título o autor)
def test_search_books():
    response = client.get("/books/search/?query=Gatsby")
    assert response.status_code == 200
    assert len(response.json()) > 0
