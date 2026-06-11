from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from database import db_connection

app=FastAPI()





















if __name__ == "__main__":
    db_connection.create_tables()
    uvicorn.run("main:app",host="127.0.0.1", port=8000, reload=True)
