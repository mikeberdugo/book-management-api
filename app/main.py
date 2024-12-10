from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request


app = FastAPI(
    title="Library Management API",  # API title
    description="This API allows managing a small library, including operations such as adding, updating, searching, and deleting books.",
    version="1.0.0",  # API version 
    
)


# Configuración de la carpeta de plantillas
templates = Jinja2Templates(directory="app/templates")  # Asegúrate de que la ruta esté correcta

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)

# Crear un nuevo libro
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book already registered")
    
    # Usar model_dump en lugar de dict
    db_book = models.Book(**book.model_dump())
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Listar todos los libros
@app.get("/books/", response_model=list[schemas.Book])
def get_books(db: Session = Depends(database.get_db)):
    # Obtener todos los libros sin ordenar explícitamente
    return db.query(models.Book).all()


# Buscar un libro por título
@app.get("/books/{title}", response_model=list[schemas.Book])
def search_books_by_title(title: str, db: Session = Depends(database.get_db)):
    return db.query(models.Book).filter(models.Book.title.ilike(f"%{title}%")).all()

# Eliminar un libro por ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


# Actualizar la información de un libro
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Actualizar solo los campos que son proporcionados
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book


# Listar todos los libros o filtrar por autor o año
@app.get("/books/", response_model=list[schemas.Book])
def get_books(author: str = None, year: int = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Book)
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year:
        query = query.filter(models.Book.year == year)
    return query.all()


# Buscar libros por título o autor
@app.get("/books/search/", response_model=list[schemas.Book])
def search_books(query: str, db: Session = Depends(database.get_db)):
    db_books = db.query(models.Book).filter(
        models.Book.title.ilike(f"%{query}%") | models.Book.author.ilike(f"%{query}%")
    ).all()
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found")
    return db_books


