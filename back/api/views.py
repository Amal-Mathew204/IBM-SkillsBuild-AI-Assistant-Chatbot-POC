"""
Module contains all the view functions for the api app
"""
import json
import os

from django.http import JsonResponse
from .WIPSemanticSearchModule.sts_module.embedding_module.controller import EmbeddingController
from .WIPSemanticSearchModule.sts_module.database.mongo_db_interface import MongoDBDatabase

# Create your views here.

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


def chatbotResponse(request) -> JsonResponse:
    """
    Method
    """
    request_body = json.loads(request.body.decode('utf-8'))
    query = request_body.get("query",None)
    k = request_body.get("k", None)
    
    # todo get data from the request body
    courses = get_top_k_courses(query, k)
    return JsonResponse(status=200,
                        data={
                            "courses": courses,
                            "text_response": "text response"
                        })
    