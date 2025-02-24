from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/<str:query>/<int:k>', views.chatbot),
]
