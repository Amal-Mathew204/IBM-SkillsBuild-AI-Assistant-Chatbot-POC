"""
Module contains all the view functions for the api app
"""
import json
import os
import django
import django.middleware
import django.middleware.csrf
import requests
from django.http import HttpRequest, JsonResponse

def create_session(request: HttpRequest):
    request.session.create()
    request.session["conversation"]=[{"role": "assistant", "content": "Welcome to the IBM Skills Build data science course assistant! To help you find the most relevant courses, I'd like to know about your educational background. Could you tell me about any degrees or qualifications you've completed?"}]
    request.session["retrieved_courses"] = []
    return django.middleware.csrf.get_token(request)
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

    csrf_token = None
    if not request.session.session_key:
        csrf_token = create_session(request)

    request.session["conversation"].append({"role": "user", "content": f"{query}"})
    print(request.session["conversation"])
    url: str = f"http://llm:{os.getenv('LLM_PORT')}/chatbot/"
    response = requests.post(url, json={
        "conversation_state": request.session["conversation"],
    })

    if response.status_code == 200:
        llm_response = response.json()
        print("LLM Response: ", llm_response)
        request.session["conversation"].append({"role": "assistant", "content": f"{llm_response['response']}"})
        print(request.session["conversation"])
        if llm_response["courses"] != []:
            request.session["retrieved_courses"].append(llm_response["courses"])
        response = JsonResponse(status=200,
                            data={"text_response": llm_response["response"],
                                  "courses": llm_response["courses"]})
    else:
        response = JsonResponse(status=500, data={"message": "Error Communicating with Internal Server"})
    request.session.modified = True
    if csrf_token != None:
        response.set_cookie(
            'csrftoken',  
            csrf_token,  
            secure=True,
            httponly=False,  
            samesite='Lax'
        )
    return response

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
    request.session["retrieved_courses"] = []
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
    csrf_token = None
    if not request.session.session_key:
        csrf_token = create_session(request)
    formatted_conversation_history = []
    count = 0
    for conversation in request.session["conversation"]:
        courses = []
        if conversation["role"] != "system":
            type = "sent"
            text = conversation["content"]
            if text == "None":
                text = ""
                courses = request.session["retrieved_courses"][count]
                count+=1
            if conversation["role"] == "assistant":
                type = "recieved"
            formatted_conversation_history.append({"text":text, "type":type, "courses":courses })
    response = JsonResponse(status=200,
                            data={
                                "chat_history": formatted_conversation_history
                            })
    if csrf_token != None:
        response.set_cookie(
            'csrftoken',  
            csrf_token,  
            secure=True,
            httponly=False,  
            samesite='Lax'
        )
    return response
    
            

