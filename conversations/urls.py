from django.urls import path
from . import views

urlpatterns = [
    path("conversations/", views.upload_conversation, name="upload_conversation"),
    path("conversations/<int:conv_id>/analyse/", views.analyze_conversation, name="analyse_conversation"),
    path("reports/", views.list_analyses, name="list_analyses"),
]
