from typing import List

from fastapi import APIRouter

from app.models import Book

router = APIRouter(prefix="/book/crud", tags=["book/crud"])


@router.post("", response_model=List[Book])
async def add_book():
    ...


@router.get("", response_model=List[Book])
async def get_books():
    ...


@router.get("/{id}", response_model=Book)
async def get_book_by_id(id: int):
    ...


@router.patch("", response_model=Book)
async def update_book(book: Book):
    ...

@router.delete("/{id}", response_model=Book)
async def delete_book(id: int):
    ...