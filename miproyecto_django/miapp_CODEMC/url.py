from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("Planes",views.planes,name="planes"),
    path("Contacto",views.contacto,name="contacto"),
    path("Inicio_login",views.inicio_usuario,name="login"),
    path("Inicio_registro_empresa", views.inicio_registro_empresa, name="registro_empresa"),
    path("Inicio_registro", views.inicio_registro, name="registro"),
    path("inicio_gestion",views.inicio_gestion,name="inicio gestion"),
    path("estadisticas",views.estadisticas,name="estadisticas"),
    path("ventas",views.ventas,name="ventas"),
    path("provedores",views.provedores,name="provedores"),
    path("libros",views.libros,name="libros"),
    path("empleados",views.empleados,name="empleados"),
    path("depositos",views.depositos,name="depositos"),
    path("configuracion",views.configuracion,name="configuracion"),
    path("compras",views.compras,name="compras"),
    path("clientes",views.clientes,name="clientes")
]
