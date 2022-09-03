from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

from model import get_segment, recognize_gov_entities, extract_components_from_sentence


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
    print('querying id =', id)
    query = "SELECT * FROM articles WHERE id={}".format(str(id))
    result = await database.fetch_one(query=query)
    return  result

@app.post("/segment")
async def fetch_segment(request: Request):
    data = await request.json()
    print(data)
    segments = []
    if 'sentence' in data:
        try:
            segments = get_segment(data['sentence'])
        except:
            pass
    return {"segment": segments}

@app.post("/ner")
async def fetch_ner(request: Request):
    data = await request.json()
    print(data)
    entities = []
    if 'sentence' in data:
        try:
            entities = recognize_gov_entities(data['sentence'])
        except:
            pass
    return {"entities": entities}

@app.post("/dep")
async def fetch_dep(request: Request):
    data = await request.json()
    print(data)
    components = []
    if 'sentence' in data:
        try:
            components = extract_components_from_sentence(data['sentence'])
        except:
            pass
    return {"components": components}
