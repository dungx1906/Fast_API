from fastapi import FastAPI
# import _json

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
# api 1
@app.get("/books/statistics")
def get_books_statistics():
    # books_statistics = []
    total_books = 0
    available_books = 0
    borrowed_books = 0
    for b in books:
        total_books += 1
        if b["is_available"] == "true":
            available_books += 1
        if b["is_available"] == "false":
            borrowed_books += 1
    return {
        "status": "ok",
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }
# api 2
@app.get("/books/categories")
def get_books_categories():
    books_categories = []
    for b in books:
        if b["category"] in books_categories:
            continue
        books_categories.append(b["category"])
    return {
        "status": "ok",
        "categories": books_categories
    }

# api 3
@app.get("/books/latest")
def get_books_latest():
    year_max = -1
    books_year_max = []
    if not books:
        return {
            "message": "No books available"
        }
    for b in books:
        if b["year"] > year_max:
            year_max = b["year"]
            books_year_max = b
    
    return {
        "status": "ok",
        "data": books_year_max
    }
    
# uvicorn main:app --reload