from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from . import forms
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

def nuevo_curso(request):
    if request.method == "POST":
        form = forms.FormularioCurso(request.POST)
        if form.is_valid():
            nombre_curso = form.cleaned_data["nombre"]
            inscriptos = form.cleaned_data["inscriptos"]
            cursor = connection.cursor()
            query = "INSERT INTO cursos (nombre_curso, inscriptos) VALUES (%s, %s)"
            cursor.execute(query, [nombre_curso, inscriptos])
            cursor.close()
            return HttpResponse("CURSO CREADO")
    else:
        form = forms.FormularioCurso()
    context = {"form": form}
    return render(request, "miapp_CODEMC/nuevo_curso.html", context)