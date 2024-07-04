from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def index(request):
    ctx = {}
    return render(request,'miapp_CODEMC/index.html',ctx)

def login_sesion(request):
    return render(request,'miapp_CODEMC/Inicio_sesion.html')

def planes(request):
    return render(request,"miapp_CODEMC/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/Contacto.html")

def listado_productos(request):
    cursor = connection.cursor()
    query = "SELECT id_prod, nom_prod FROM `productos` ORDER BY id_prod, nom_prod"
    cursor.execute(query)
    products=cursor.fetchall()

    

    ctx={"prods":products
         }

    connection.close()  # Cerrar la conexion
    
    return render(request,'miapp_CODEMC/prueba_fetchall.html',ctx)