from fastapi import FastAPI

app = FastAPI()

@app.get("/heath")
def heath():
    print("API đang chạy")