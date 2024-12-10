import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas import BookCreate, BookUpdate

# Configuración para la base de datos de pruebas en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Usamos SQLite en disco, o puedes usar en memoria "sqlite:///:memory:"

# Crear un motor y una sesión para las pruebas
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas para las pruebas
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación de pruebas
app.dependency_overrides[database.get_db] = lambda: TestingSessionLocal()

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    # Crear una nueva sesión de base de datos antes de cada prueba
    db = TestingSessionLocal()
    yield db
    db.close()
    # Limpiar la base de datos después de cada prueba
    db.query(models.Book).delete()
    db.commit()


def test_create_book():
    # Datos del libro para crear
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2023,
        "isbn": "1234567890"
    }

    # Hacer la solicitud POST para crear un libro
    response = client.post("/books/", json=book_data)
    
    # Verificar que la respuesta sea exitosa
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    assert response.json()["author"] == book_data["author"]
    assert response.json()["year"] == book_data["year"]
    assert response.json()["isbn"] == book_data["isbn"]


def test_update_book():
    # Crear un libro primero
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2023,
        "isbn": "1234567890"
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Datos para actualizar el libro
    updated_data = {
        "title": "Updated Book Title",
        "author": "Updated Author",
        "year": 2024,
        "isbn": "0987654321"
    }

    # Hacer la solicitud PUT para actualizar el libro
    update_response = client.put(f"/books/{book_id}", json=updated_data)
    
    # Verificar que la respuesta sea exitosa
    assert update_response.status_code == 200
    assert update_response.json()["title"] == updated_data["title"]
    assert update_response.json()["author"] == updated_data["author"]
    assert update_response.json()["year"] == updated_data["year"]
    assert update_response.json()["isbn"] == updated_data["isbn"]


def test_delete_book():
    # Crear un libro primero
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2023,
        "isbn": "1234567890"
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Hacer la solicitud DELETE para eliminar el libro
    delete_response = client.delete(f"/books/{book_id}")
    
    # Verificar que la respuesta sea exitosa
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Book deleted successfully"}

    # Intentar obtener el libro eliminado
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Book not found"}


def test_get_books():
    # Crear libros para obtener
    book_data_1 = {"title": "Book 1", "author": "Author 1", "year": 2022, "isbn": "1111111111"}
    book_data_2 = {"title": "Book 2", "author": "Author 2", "year": 2023, "isbn": "2222222222"}
    
    client.post("/books/", json=book_data_1)
    client.post("/books/", json=book_data_2)

    # Hacer la solicitud GET para obtener todos los libros
    response = client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 2


def test_search_books_by_title():
    # Crear un libro para búsqueda
    book_data = {"title": "Unique Book", "author": "Author", "year": 2023, "isbn": "1234567890"}
    client.post("/books/", json=book_data)

    # Buscar el libro por título
    response = client.get("/books/search/", params={"query": "Unique"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Unique Book"


def test_search_books_by_author():
    # Crear un libro para búsqueda
    book_data = {"title": "Book by Author", "author": "Famous Author", "year": 2023, "isbn": "1234567890"}
    client.post("/books/", json=book_data)

    # Buscar el libro por autor
    response = client.get("/books/search/", params={"query": "Famous"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["author"] == "Famous Author"


def test_get_books_by_author_and_year():
    # Crear libros con autores y años diferentes
    book_data_1 = {"title": "Book 1", "author": "Author 1", "year": 2022, "isbn": "1111111111"}
    book_data_2 = {"title": "Book 2", "author": "Author 2", "year": 2023, "isbn": "2222222222"}
    
    client.post("/books/", json=book_data_1)
    client.post("/books/", json=book_data_2)

    # Obtener libros filtrados por autor
    response = client.get("/books/", params={"author": "Author 1"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["author"] == "Author 1"

    # Obtener libros filtrados por año
    response = client.get("/books/", params={"year": 2023})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["year"] == 2023
