from http import HTTPStatus
from typing import Optional
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    year: int

    def __init__(self, id, title, author, description, rating, year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.year = year


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    year: int = Field(gt=1950, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book title",
                "author": "Author name",
                "description": "Describe what is the book about",
                "rating": 3,
                "year": 2020
            }
        }
    }


BOOKS: list[Book] = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def read_book(id: int = Path(gt=0)):
    books: list[Book] = [b for b in BOOKS if id == b.id]
    book = books[0] if len(books) > 0 else None

    if book is not None:
        return book

    raise HTTPException(status_code=404, detail='Book not found')


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(
        book_rating: int = Query(gt=-1, lt=6, default=None),
        book_year: int = Query(gt=1950, lt=2031, default=None)):
    books_to_return = BOOKS
    if book_rating is not None:
        books_to_return = [b for b in books_to_return if b.rating == book_rating]

    if book_year is not None:
        books_to_return = [b for b in books_to_return if b.year == book_year]

    if len(books_to_return) > 0:
        return books_to_return

    raise HTTPException(status_code=404, detail='Books not found')


@app.post("/booksWithBody", status_code=status.HTTP_201_CREATED)
async def create_book_with_body(book_request=Body()):
    BOOKS.append(book_request)


@app.post("/booksWithPydentic", status_code=status.HTTP_204_NO_CONTENT)
async def create_book_with_pydantic(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_202_ACCEPTED)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
