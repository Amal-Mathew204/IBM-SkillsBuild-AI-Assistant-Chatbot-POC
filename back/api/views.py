"""
Module contains all the view functions for the api app
"""
import json
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
        request.session["conversation"]=[{"role": "assistant", "content": "Welcome to the IBM Skills Build data science course assistant! To help you find the most relevant courses, I'd like to know about your educational background. Could you tell me about any degrees or qualifications you've completed?"}]
    request.session["input_count"] = request.session["input_count"] + 1
    print("REQUEST SESSION",request.session["input_count"])

    # url: str = f"http://semanticsearch:{os.getenv('SEMANTIC_SEARCH_PORT')}/{query}/{k}"
    # print(url)
    # response = requests.get(url, timeout=30)
    # print("Response")
    # print(response.status_code)
    # print(response.text)
    # if response.status_code == 200:
    #     courses = response.json()
    #     return JsonResponse(status=200,
    #                         data={
    #                             "courses": courses,
    #                             "text_response": "text response"
    #                         })

    request.session["conversation"].append({"role": "user", "content": f"{query}"})
    print(request.session["conversation"])
    url: str = f"http://llm:{os.getenv('LLM_PORT')}/chatbot/"
    response = requests.post(url, json={
        "conversation_state": request.session["conversation"],
    })

    if response.status_code == 200:
        llm_response = response.json()
        print(llm_response)
        request.session["conversation"].append({"role": "assistant", "content": f"{llm_response['response']}"})
        return JsonResponse(status=200,
                            data={"text_response": llm_response["response"],
                                  "courses": llm_response["courses"]})
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
    course_info = json.loads(request.body.decode("utf-8"))["course"]
    url: str = f"http://reversesearch:{os.getenv('REVERSE_SEARCH_PORT')}/"
    print(url)
    response = requests.post(url, json=course_info, timeout=30)
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

def reset_chat(request: HttpRequest):
    """
    Method
    """
    if request.method != "PUT":
        return
    request.session["conversation"]=[{"role": "assistant", "content": "Welcome to the IBM Skills Build data science course assistant! To help you find the most relevant courses, I'd like to know about your educational background. Could you tell me about any degrees or qualifications you've completed?"}]
    return JsonResponse(status=200,
                            data={
                                "message": "chat reset sucessfully"
                            })

def fetch_chat(request: HttpRequest):
    """
    Method
    """

    if request.method != "GET":
        return
    if not request.session.session_key:
        request.session.create()
        request.session["input_count"]=0
        request.session["conversation"]=[{"role": "assistant", "content": "Welcome to the IBM Skills Build data science course assistant! To help you find the most relevant courses, I'd like to know about your educational background. Could you tell me about any degrees or qualifications you've completed?"}]
    formatted_conversation_history = []
    for conversation in request.session["conversation"]:
        if conversation["role"] != "system":
            type = "sent"
            text = conversation["content"]
            if conversation["role"] == "assistant":
                type = "recieved"
            formatted_conversation_history.append({"text":text, "type":type})
    return JsonResponse(status=200,
                            data={
                                "chat_history": formatted_conversation_history
                            })
            

