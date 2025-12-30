from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel 
from fastapi import APIRouter, status,Depends
from fastapi.exceptions import HTTPException
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/")
async def read_item(name: Optional[str] = None):
    return {"name": name} 


class Book(BaseModel):
    title: str
    author: str
    year: int

books=[
    {
        "id":1,
        "title":"The Great Gatsby",
        "author":"F. Scott Fitzgerald",
        "year":1925
    },
    {
        "id":2,
        "title":"To Kill a Mockingbird",
        "author":"Harper Lee",
        "year":1960                     
        
    },
    {
        "id":3,
        "title":"1984",
        "author":"George Orwell",
        "year":1949
    },
    {
        "id":4,
        "title":"Pride and Prejudice",
        "author":"Jane Austen",
        "year":1813
    },
    {
        "id":5,
        "title":"The Catcher in the Rye",
        "author":"J.D. Salinger",
        "year":1951
    }
    
]


@app.get("/books/")
async def get_books():
    return books    


@app.post("/books/")
async def add_book(book: Book):
    books.append(book.dict())
    return book 


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):            
    
    for index, book in enumerate(books):
        if book["id"] == book_id:
            del books[index]
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = updated_book.dict()
            books[index]["id"] = book_id  # Ensure the ID remains unchanged
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")


# this is completely plain crud operations