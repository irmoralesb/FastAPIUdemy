from fastapi import FastAPI, Body
from pydantic import BaseModel

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
    id: int
    title: str
    author: str
    description: str
    rating: int
    year: int


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/booksWithBody")
async def create_book_with_body(book_request=Body()):
    BOOKS.append(book_request)


@app.post("/booksWithPydentic")
async def create_book_with_pydantic(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
