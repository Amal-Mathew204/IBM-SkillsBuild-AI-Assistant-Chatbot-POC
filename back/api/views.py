"""
Module contains all the view functions for the api app
"""
import os
import requests
from django.http import HttpRequest, JsonResponse


def chatbot(request: HttpRequest, query: str, k: int) -> JsonResponse:
    """
    Method
    """
    #TODO change to invalid method response
    if request.method != "GET":
        return
    # TODO valididate inputs
    # also do exception handling cause ibr the semantic search container is slow
    # (so making early requests will cause exceptions)
    # and just do overall handling of bad requests

    if not request.session.session_key:
        request.session.create()
        request.session["input_count"]=0
    request.session["input_count"] = request.session["input_count"] + 1
    print("REQUEST SESSION",request.session["input_count"])

    url: str = f"http://semanticsearch:{os.getenv('SEMANTIC_SEARCH_PORT')}/{query}/{k}"
    print(url)
    response = requests.get(url, timeout=30)
    print("Response")
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        courses = response.json()
        return JsonResponse(status=200,
                            data={
                                "courses": courses,
                                "text_response": "text response"
                            })
    return JsonResponse(status=500,
                        data={"detail": "(Error communicating with interval servers"})


def get_similar_courses(request: HttpRequest) -> JsonResponse:
    """
    Method
    """
    #TODO change to invalid method response
    if request.method != "POST":
        return
    # TODO valididate inputs
    # also do exception handling
    # (so making early requests will cause exceptions)
    # and just do overall handling of bad requests
    course_info = request.data["course"]
    url: str = f"http://reversesearch:{os.getenv('REVERSE_SEARCH_PORT')}/"
    print(url)
    response = requests.post(url, data=course_info, timeout=30)
    print("Response")
    print(response.status_code)
    print(response.text)
    if response.status_code == 200:
        courses = response.json()
        return JsonResponse(status=200,
                            data={
                                "similar_courses": courses
                            })
    return JsonResponse(status=500,
                        data={"detail": "(Error communicating with interval servers"})
    