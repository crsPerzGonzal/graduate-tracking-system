from django.urls import path 
from . import views

urlpatterns = [
    path("", views.chat_view, name ="chat"),
    path("<int:session_id>/", views.chat_view, name="chat_con_id"),
    path("buscar/", views.buscar_conversaciones, name="buscar_conversaciones"),
]