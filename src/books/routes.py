from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel 
from fastapi import APIRouter, status,Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, BookUpdateModel
from src.books.book_data import books
from fastapi import APIRouter

book_router = APIRouter()





@book_router.get("/")
async def get_books():
    return books    


@book_router.post("/")
async def add_book(book: Book):
    books.append(book.dict())
    return book 


@book_router.get("/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/{book_id}")
async def delete_book(book_id: int):            
    
    for index, book in enumerate(books):
        if book["id"] == book_id:
            del books[index]
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.put("/{book_id}")
async def update_book(book_id: int, updated_book: BookUpdateModel):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = updated_book.dict()
            books[index]["id"] = book_id  # Ensure the ID remains unchanged
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")