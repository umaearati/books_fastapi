# pip install sqlmodel
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config import config
from sqlalchemy import text  


engine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True
)
      
      
async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hello world'")
        result = await conn.execute(statement)
        
        print(result.all())    