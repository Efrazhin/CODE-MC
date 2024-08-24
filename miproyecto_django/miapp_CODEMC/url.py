from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("Planes",views.planes,name="planes"),
    path("Contacto",views.contacto,name="contacto"),
    path("Inicio_login",views.inicio_usuario,name="login"),
    path("Inicio_registro", views.inicio_registro, name="registro")
]