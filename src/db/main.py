# pip install sqlmodel
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config import config
from sqlalchemy import text  
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True
)
      
      
# async def init_db():
#     async with engine.begin() as conn:
#         statement = text("SELECT 'hello world'")
#         result = await conn.execute(statement)
        
#         print(result.all()) 

# this code to test connection btw db n app


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book  # Import models to register them with SQLModel metadata  
        await conn.run_sync(SQLModel.metadata.create_all)    
        
        
# this code is for 1st table books  
# psql 'postgresql://neondb_owner:npg_oBm2NCk5RsPD@ep-muddy-hat-a4ww4nul-pooler.us-east-1.aws.neon.tech/bookly_db?sslmode=require&channel_binding=require'  
#  \c bookly_db - connected to database 
# \dt tables in db
#  \d books
# DROP TABLE books ;  -- to drop table


async def get_session() -> AsyncSession:
    session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with session() as session:
        yield session
    





       