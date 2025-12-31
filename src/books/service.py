from datetime import datetime
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class BookService:
    async def get_all_books(self, session: AsyncSession) -> list[Book]:
        statement = select(Book).order_by(Book.created_at.desc())
        result = await session.execute(statement)   # ✅ use execute()
        books = result.scalars().all()             # ✅ extract ORM objects
        return books

    # async def get_user_books(self, user_uid: str, session: AsyncSession):
    #     statement = (
    #         select(Book)
    #         .where(Book.user_uid == user_uid)
    #         .order_by(desc(Book.created_at))
    #     )

    #     result = await session.exec(statement)

    #     return result.all()


    async def get_book(self, book_uid: str, session: AsyncSession) -> Book | None:
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)   # ✅ use execute()
        book = result.scalars().one_or_none()       # ✅ extract ORM object
        return book 


    async def create_book(
        self, book_data: BookCreateModel, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )

        # new_book.user_uid = user_uid

        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ) -> Book:
        # Fetch the book
        book_to_update = await self.get_book(book_uid, session)

        if not book_to_update:
            raise HTTPException(status_code=404, detail="Book not found")

        # Convert Pydantic model to dict, only update fields that were set
        update_data_dict = update_data.model_dump(exclude_unset=True)

        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)

        # Commit changes and refresh to get updated object
        await session.commit()
        await session.refresh(book_to_update)

        return book_to_update


    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()

            return {}

        else:
            return None