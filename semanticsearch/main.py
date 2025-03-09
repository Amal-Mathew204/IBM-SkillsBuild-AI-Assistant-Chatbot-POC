"""
Fast API main.py defining the API endpoint to access the semantic search module
"""
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sts_module.database.mongo_db_interface import MongoDBDatabase
from sts_module.embedding_module.controller import EmbeddingController
from setup import database_setup_embedded_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    "Method for executing setup code for the semantic search module"
    url: str = f"mongodb://{os.getenv('MONGO_CONTAINER')}:{os.getenv('MONGO_PORT')}/"
    database_setup_embedded_database(
                url=url,
                username=os.getenv('MONGO_USER'),
                password=os.getenv('MONGO_PASSWORD'),
                database_auth_mechanism=os.getenv('MONGO_AUTH_MECHANISM'),
                database_name=os.getenv('MONGO_CHATBOT_DATABASE'),
                courses_collection_name=os.getenv('MONGO_COURSE_COLLECTION'),
                embedded_dataset_collection_name=os.getenv('MONGO_EMBEDDED_DATASET_COLLECTION')
            )
    yield

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

def get_top_k_courses(query: str, k: int) -> list[dict]:
    """
    Method calls the semantic search module to calling the `courses_semantic_search`
    to obtain the top k courses with the greatest semantic relation to the users query.

    Args: 
        query (str): User Input query to obtain courses
        k (int): Top number of courses to be returned by the semantic search module

    Returns: 
        list[dict]: list of top k courses (information stored as a dict object)
    """
    url: str = f"mongodb://{os.getenv('MONGO_CONTAINER')}:{os.getenv('MONGO_PORT')}/"
    #Database Object connecting to the Courses Collection
    courses_database = MongoDBDatabase(
                url=url,
                username=os.getenv('MONGO_USER'),
                password=os.getenv('MONGO_PASSWORD'),
                auth_mechanism=os.getenv('MONGO_AUTH_MECHANISM'),
                database=os.getenv('MONGO_CHATBOT_DATABASE'),
                collection=os.getenv('MONGO_COURSE_COLLECTION'))
    #Database Object connecting to the Embedded Dataset Collection
    embedded_database = MongoDBDatabase(
                    url=url,
                    username=os.getenv('MONGO_USER'),
                    password=os.getenv('MONGO_PASSWORD'),
                    auth_mechanism=os.getenv('MONGO_AUTH_MECHANISM'),
                    database=os.getenv('MONGO_CHATBOT_DATABASE'),
                    collection=os.getenv('MONGO_EMBEDDED_DATASET_COLLECTION'))
    controller = EmbeddingController(courses_database, embedded_database)
    return controller.courses_semantic_search(query, k)


@app.get("/{query}/{k}")
def main(query: str, k: int) -> list[dict]:
    """
    Method is the API Endpoint function to perform semantic search

    Args:
        query (str): User Input query to obtain courses
        k (int): Top number of courses to be returned by the semantic search module
    Returns: 
        list[dict]: list of top k courses (information stored as a dict object) 
    """
    if query == "":
        raise HTTPException(status_code=422, detail="Query String must not be empty")
    if k <= 0:
        raise HTTPException(status_code=422,
                            detail="Number of courses returned must be greater than zero")
    return get_top_k_courses(query=query, k=k)
