from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

# FastAPI application initialization
app = FastAPI(
    title="Library Management API",  # Title of the API
    description="This API allows managing a small library, including operations such as adding, updating, searching, and deleting books.",  # Description of what the API does
    version="1.0.0",  # API version
)

# Configure the folder for HTML templates
templates = Jinja2Templates(directory="app/templates")  # Ensure the path is correct

# Endpoint to serve the home page with HTML response
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

# Endpoint to create a new book
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book already registered")  # If book already exists, raise error
    
    # Use model_dump to create a new book from the schema
    db_book = models.Book(**book.model_dump())
    
    db.add(db_book)  # Add new book to the session
    db.commit()  # Commit the transaction to the database
    db.refresh(db_book)  # Refresh the book instance
    return db_book  # Return the created book

# Endpoint to list all books
@app.get("/books/", response_model=list[schemas.Book])
def get_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).all()  # Return all books from the database

# Endpoint to search for books by title
@app.get("/books/{title}", response_model=list[schemas.Book])
def search_books_by_title(title: str, db: Session = Depends(database.get_db)):
    return db.query(models.Book).filter(models.Book.title.ilike(f"%{title}%")).all()  # Search for books matching the title

# Endpoint to delete a book by ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()  # Find book by ID
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")  # If book not found, raise error
    db.delete(db_book)  # Delete the book from the database
    db.commit()  # Commit the transaction
    return {"message": "Book deleted successfully"}  # Return success message

# Endpoint to update a book's information by ID
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()  # Find book by ID
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")  # If book not found, raise error
    
    # Update only the fields provided in the request
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    db.commit()  # Commit the transaction
    db.refresh(db_book)  # Refresh the book instance
    return db_book  # Return the updated book

# Endpoint to list books with optional filters for author or year
@app.get("/books/", response_model=list[schemas.Book])
def get_books(author: str = None, year: int = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Book)  # Start query for all books
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))  # Filter by author if provided
    if year:
        query = query.filter(models.Book.year == year)  # Filter by year if provided
    return query.all()  # Return filtered books

# Endpoint to search books by either title or author
@app.get("/books/search/", response_model=list[schemas.Book])
def search_books(query: str, db: Session = Depends(database.get_db)):
    db_books = db.query(models.Book).filter(
        models.Book.title.ilike(f"%{query}%") | models.Book.author.ilike(f"%{query}%")
    ).all()  # Search books by title or author
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found")  # If no books found, raise error
    return db_books  # Return found books
