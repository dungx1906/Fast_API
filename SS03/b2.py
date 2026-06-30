from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Lê Minh Thu",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Phạm Lan Hồng",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Lê Minh Huyền",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Lê Ánh Linh",
        "category": "programming",
        "year": 2008,
        "is_available": False
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vũ Hồng Vân",
        "category": "network",
        "year": 2019,
        "is_available": True
    }
]
@app.get("/books/available")
def get_books_available():
    books_available = []
    for b in books:
        if b["is_available"]:
            books_available.append(b)
    return {
        "message": "Danh sách còn có thể mượn",
        "books": books_available
    }
@app.get("/books/borrowed")
def get_books_borrowed():
    books_borrowed = []
    for b in books:
        if not b["is_available"]:
            books_borrowed.append(b)
    return {
        "message": "Danh sách đang được mượn",
        "books": books_borrowed
    }
    