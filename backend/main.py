from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Sandbox_AI Backend is running!"}