#TODO use pylint doc string this file
from contextlib import asynccontextmanager
from es_client import create_index, get_es_client, index_documents, search_similar_courses
from db import fetch_documents
from fastapi import FastAPI
from pydantic import BaseModel
import os


class Course(BaseModel):
    #TODO: need to fill our the rest of the fields of an expected IBM SkillsBuild Course JSON Object
    title: str
    description: str
    learning_hours: str
    course_type: str
    tags: list
    url: str 

es_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    es_client = get_es_client()
    create_index(es_client, "courses_index")
    documents = fetch_documents(os.getenv('MONGO_COURSE_COLLECTION'))
    index_documents(es_client, "courses_index", documents)
    yield
    es_client.close()

app = FastAPI(lifespan=lifespan)


@app.post("/")
def search_courses(course: Course):
    es_client = get_es_client()
    results = search_similar_courses(es_client, "courses_index", dict(course))
    courses = [hit['_source'] for hit in results['hits']['hits']]
    return courses