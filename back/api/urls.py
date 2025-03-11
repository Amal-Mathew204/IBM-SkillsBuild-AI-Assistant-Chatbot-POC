from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/<str:query>/<int:k>', views.chatbot),
    path('similarcourses/', views.get_similar_courses),
]