
from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("pricing-tiers/",views.planes,name="planes"),
    path("contact/",views.contacto,name="contacto"),
    path("login/",views.user_login,name="login"),
    path("logout/",views.user_signout,name="logout"),
    path("user-registration/", views.user_registration, name="registro-usuario"),
    path("home/",views.inicio_gestion,name="home"),
    path("estadisticas/",views.estadisticas,name="estadisticas"),
    path("ventas/",views.ventas,name="ventas"),
    path("provedores/",views.provedores,name="provedores"),
    path("libros/",views.libros,name="libros"),
    path("employees/",views.empleados,name="empleados"),
    path("employee-registration/",views.user_registration,name="crear-empleado"),
    path("depositos/",views.depositos,name="depositos"),
    path("configuracion/",views.configuracion,name="configuracion"),
    path("compras/",views.compras,name="compras"),
    path("clientes/",views.clientes,name="clientes"),
    path("categorias/",views.categorias_view,name="categorias"),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path("agregar_producto/",views.agregar_productos, name='agrear-producto'),
    path('crear_almacen/', views.crear_almacen, name='crear_almacen'),
    path("crear_sucursal/",views.crear_sucursal, name="crear_sucursal"),
    path('eliminar-almacen/<int:id_almacen>/', views.eliminar_almacen, name='eliminar_almacen'),
    path('eliminar-sucursal/<int:id_sucursal>/', views.eliminar_sucursal, name='eliminar_sucursal')
]
