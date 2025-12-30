from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup code can go here")
    await init_db()
    yield
    print("Shutdown code can go here")

version="v1"

app = FastAPI(
    version=version,
    title="Book Management API",
    description="API for managing a collection of books",
    lifespan=lifespan
) 

app.include_router(book_router,prefix="/books",tags=["books"])

# this is my first commit 
