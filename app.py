from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import requests

app = FastAPI()

load_dotenv()

@app.get("/script.js")
def script():
    return FileResponse("script.js")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/search")
def search(query):
    api_key = os.getenv("SERPER_API_KEY")

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "q": query,
        "num": 10,
        "page": 1
    }

    response = requests.post(
        "https://google.serper.dev/search",
        headers=headers,
        json=data
    )

    try:
        result = response.json()
        return result["organic"]
    except Exception:
        raise HTTPException(status_code=500, detail="Error during search")