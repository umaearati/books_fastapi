from fastapi import FastAPI
from src.books.routes import book_router

version="v1"

app = FastAPI(
    version=version,
    title="Book Management API",
    description="API for managing a collection of books"
) 

app.include_router(book_router,prefix="/books",tags=["books"])

# this is my first commit 
