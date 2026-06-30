from fastapi import FastAPI

app = FastAPI()

students = ["An", "Binh", "Cuong"]
@app.get("/students")
def get_students():
    return {
        "data": students
    }