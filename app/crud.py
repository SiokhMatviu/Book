from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/book/crud", tags=["book/crud"])


@router.post("", response_model=BookCreate)
async def add_book(
    data: Annotated[BookCreate, Depends()],
    session: AsyncSession = Depends(get_db)
):
    book =Book(
        title=data.title,
        author=data.author,
        year=data.year
    )

    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book


@router.get("", response_model=list[BookResponse])
async def get_books(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * size

    stmt = (
        select(Book)
        .limit(size)
        .offset(offset)
    )

    items = (await session.execute(stmt)).scalars().all()

    return items


@router.get("/{id}", response_model=BookResponse)
async def get_book_by_id(
    id: int,
    session: AsyncSession = Depends(get_db)
):
    book = await session.get(Book, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book



@router.patch("/{id}", response_model=BookUpdate)
async def update_book(
    id: int,
    data: Annotated[BookUpdate, Depends()],
    session: AsyncSession = Depends(get_db)
):
    book = await session.get(Book, id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if data.title is not None:
        book.title = data.title

    if data.author is not None:
        book.author = data.author

    if data.year is not None:
        book.year = data.year

    await session.commit()
    await session.refresh(book)

    return book


@router.delete("/{id}")
async def delete_book(
    id: int,
    session: AsyncSession = Depends(get_db)
):
    book = await session.get(Book, id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(book)
    await session.commit()

    return {
        "status": "success"
    }