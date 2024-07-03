from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("login",views.login_sesion,name="login"),
    path("listado_productos",views.listado_productos,name="listado_stock"),
    path("Planes",views.planes,name="planes"),
    path("Contacto",views.contacto,name="contacto")
]