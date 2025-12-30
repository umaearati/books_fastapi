from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    
    
class BookUpdateModel(BaseModel):
    title: Optional[str] = None   
    author: str
    year: int
    
    
    