from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

from nlp_api import get_segment, recognize_gov_entities, extract_components_from_sentence


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

# insert record
@app.post("/insert")
async def insert_data(request: Request):
    data = await request.json()
    assert 'title' in data
    print('inserting data', data)
    result = await database.execute(
        query="INSERT INTO articles(title, publish_date, content)\
               VALUES (:title, :publish_date, :content)",
        values={
            'title': data['title'],
            'publish_date': data.get('publish_date', ''),
            'content': data.get('content', ''),
        })
    print('new record id =', result)
    return  result

# query on id
@app.get("/article")
async def fetch_data(id: int):
    print('querying id =', id)
    query = "SELECT * FROM articles WHERE id={}".format(str(id))
    result = await database.fetch_one(query=query)
    print(result)
    return  result

# task1 
@app.post("/segment")
async def fetch_segment(request: Request):
    data = await request.json()
    print(data)
    segments = []
    if 'sentence' in data:
        try:
            segments = get_segment(data['sentence'])
        except Exception as e:
            print(e)
    return {"segment": segments}

# task2
@app.post("/ner")
async def fetch_ner(request: Request):
    data = await request.json()
    print(data)
    entities = []
    if 'sentence' in data:
        try:
            entities = recognize_gov_entities(data['sentence'])
        except Exception as e:
            print(e)
    return {"entities": entities}

# task3
@app.post("/dep")
async def fetch_dep(request: Request):
    data = await request.json()
    print(data)
    components = []
    if 'sentence' in data:
        try:
            components = extract_components_from_sentence(data['sentence'])
        except Exception as e:
            print(e)
    return {"components": components}
