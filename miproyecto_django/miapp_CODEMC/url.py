from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("pricing-tiers/",views.planes,name="planes"),
    path("contact/",views.contacto,name="contacto"),
    path("login/",views.user_login,name="login"),
    path("logout/",views.user_signout,name="logout"),
    path("company-registration/", views.company_registration, name="registro_empresa"),
    path("user-registration/", views.user_registration, name="registro-usuario"),
    path("home/",views.inicio_gestion,name="home"),
    path("estadisticas/",views.estadisticas,name="estadisticas"),
    path("ventas/",views.ventas,name="ventas"),
    path("provedores/",views.provedores,name="provedores"),
    path("libros/",views.libros,name="libros"),
    path("empleados/",views.empleados,name="empleados"),
    path("depositos/",views.depositos,name="depositos"),
    path("configuracion/",views.configuracion,name="configuracion"),
    path("compras/",views.compras,name="compras"),
    path("clientes/",views.clientes,name="clientes"),
    path("categorias/",views.categorias_view,name="categorias"),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria')
]
