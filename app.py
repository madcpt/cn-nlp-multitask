from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

app = FastAPI()

database = Database("sqlite:///data/data.db")

@app.on_event("startup")
async def database_connect():
    await database.connect()

@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/article")
async def fetch_data(id: int):
    query = "SELECT * FROM articles WHERE id={}".format(str(id))
    result = await database.fetch_one(query=query)
    return  result