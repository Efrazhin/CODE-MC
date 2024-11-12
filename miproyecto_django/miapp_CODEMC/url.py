
from django.urls import path
from . import views

urlpatterns=[
    path("", views.index,name="index"),
    path("pricing-tiers/",views.planes,name="planes"),
    path("contact/",views.contacto,name="contacto"),

    path("login/",views.user_login,name="login"),
    path("logout/",views.user_signout,name="logout"),
    path("user-registration/", views.user_registration, name="registro-usuario"),

    path("home/",views.home,name="home"),
    path("estadisticas/",views.estadisticas,name="estadisticas"),
    path("ventas/",views.ventas,name="ventas"),

    path("suppliers/",views.proveedores,name="proveedores"),
    path("suppliers/add-supplier",views.agregar_proveedor,name="agregar-proveedor"),

    path("libros/",views.libros,name="libros"),

    path("employees/",views.empleados,name="empleados"),
    path("employees/registration/",views.user_registration,name="crear-empleado"),

    path("warehouses/",views.almacenes,name="almacenes"),
    path("configuracion/",views.configuracion,name="configuracion"),

    path("customers/",views.clientes,name="clientes"),
    path("customers/add-customer",views.agregar_cliente,name="agregar-cliente"),

    path("purchases/",views.compras,name="compras"),
    path("purchases/add-remmitance/",views.agregar_compra,name="agregar_compra"),
    path("purchases/add-remmitance/del-remmitance",views.cancelar_proceso_venta_compra,name="cancelar_compra"),
    path("purchases/add-remmitance/add-detail",views.agregar_detalle,name="agregar_detalle_compra"),
    path("purchases/add-remmitance/del-detail/<str:producto_cod>/",views.sacar_detalle,name="eliminar_detalle"),
    path("purchases/details/<int:remito_id>",views.obtener_detalles,name="get_detalles"),


    path("sales/",views.ventas,name="ventas"),
    path("sales/add-remmitance/",views.agregar_venta,name="agregar-venta"),
    path("sales/add-remmitance/del-remmitance",views.cancelar_proceso_venta_compra,name="cancelar_venta"),
    path("sales/add-remmitance/add-detail",views.agregar_detalle,name="agregar_detalle_venta"),
    path("sales/add-remmitance/del-detail/<str:producto_cod>/",views.sacar_detalle,name="eliminar_detalle"),
    path("sales/details/<int:remito_id>/",views.obtener_detalles,name="get_detalles"),

    path("categories/",views.categorias_subcategorias_productos,name="categorias"),
    path('categories/add-category/', views.crear_categoria, name='crear_categoria'),

    path("products/add-product/",views.agregar_productos, name='agregar-producto'),
    path("products/", views.productos_view, name='productos'),
    path('eliminar_producto/<str:producto_cod>/', views.eliminar_producto, name='eliminar_producto'),

    path('crear_almacen/', views.crear_almacen, name='crear_almacen'),
    path("crear_sucursal/",views.crear_sucursal, name="crear_sucursal"),
    path('eliminar-almacen/<int:id_almacen>/', views.eliminar_almacen, name='eliminar_almacen'),
    path('eliminar-sucursal/<int:id_sucursal>/', views.eliminar_sucursal, name='eliminar_sucursal'),
    
]
