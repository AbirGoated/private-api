from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Personal API is running!"}