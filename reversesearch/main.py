"""Module ..."""
#TODO use pylint doc string this file
import os
from contextlib import asynccontextmanager
from es_client import create_index, get_es_client, index_documents, search_similar_courses
from db import fetch_documents
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Course(BaseModel):
    """Class ..."""
    title: str
    description: str
    learning_hours: str
    course_type: str
    tags: list
    url: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Method ..."""
    print("Start Up Process")
    app.es_client = get_es_client()
    create_index(app.es_client, "courses_index")
    documents = fetch_documents(os.getenv('MONGO_COURSE_COLLECTION'))
    print("Documents retrieved from DB: ", len(documents))
    index_documents(app.es_client, "courses_index", documents)
    print("Start Up Process Finished")
    yield
    app.es_client.close()

app = FastAPI(lifespan=lifespan)

origins=[
    f"http://{os.getenv('HOST')}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.post("/")
def search_courses(course: Course):
    """Method ..."""
    results = search_similar_courses(app.es_client, "courses_index", dict(course))# pylint: disable = no-member
    print(results)
    courses = [hit['_source'] for hit in results['hits']['hits']]
    return courses
