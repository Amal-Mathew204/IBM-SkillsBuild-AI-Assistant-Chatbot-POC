"""
Module contains all the view functions for the api app
"""
import requests
from django.http import JsonResponse


def chatbot(request, query: str, k: int) -> JsonResponse:
    """
    Method
    """
    #TODO change to invalid method response
    if request.method != "GET":
        return
    # TODO valididate inputs
    # put ports in env files to
    # also do exception handling cause ibr the semantic search container is slow
    # (so making early requests will cause exceptions)
    url: str = f"http://nginx:80/search/{query}/{k}"
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
    