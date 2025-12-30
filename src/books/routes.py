from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel 
from fastapi import APIRouter, status,Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, BookUpdateModel
from fastapi import APIRouter
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()

@book_router.get("/",response_model=list[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books    


@book_router.post("/")
async def add_book(book_data: Book, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data, session) 
    return new_book


@book_router.get("/{book_uid}")
async def get_book(book_uid: int, session: AsyncSession = Depends(get_session)):
   book = await book_service.get_book(book_uid, session)
   if book:
       return book
   else:    
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/{book_uid}")
async def delete_book(book_uid: int, session: AsyncSession = Depends(get_session)):            
    
    deleted_book = await book_service.delete_book(book_uid, session)
    if deleted_book:
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@book_router.patch("/{book_uid}")
async def update_book(book_uid: int, updated_book: BookUpdateModel, session: AsyncSession = Depends(get_session)):
    update_book = await book_service.update_book(book_uid, updated_book, session)
    if update_book:
        return update_book
    else:        
     raise HTTPException(status_code=404, detail="Book not found") 
    