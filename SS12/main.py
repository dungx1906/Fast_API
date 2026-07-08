from fastapi import FastAPI

app = FastAPI()

@app.get("/health", tags=["Health"])
def det_health():
    return{
        "message":"i'm fine..."
    }