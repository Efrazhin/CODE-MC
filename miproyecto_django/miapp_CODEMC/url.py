from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("login",views.login_sesion,name="login"),
    path("prueba_listado",views.listado_productos,name="listado_stock"),
    path("Planes",views.planes,name="planes"),
    path("Contacto",views.contacto,name="contacto"),
    path("nuevo_curso",views.nuevo_curso,name="nuevocurso"),
    path("Inicio_login",views.inicio_usuario,name="iniciologin"),
]