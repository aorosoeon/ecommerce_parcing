from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

@app.get("/scrape")
async def scrape():
    try:
        result = subprocess.run(['python', 'scraper.py'], 
                              capture_output=True, 
                              text=True)
        return {
            "status": "success",
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }