from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.urls import reverse
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
            cursor = connection.cursor()
            query = "INSERT INTO cursos VALUES(null, ?, ?)", (form.cleaned_data["nombre"], form.cleaned_data["inscriptos"])
            cursor.execute(query)
            connection.commit()
            connection.close()
            return HttpResponse("Curso creadooooo")
    else:
        form = forms.FormularioCurso()

    ctx = {"form": form}
    return render(request, "miapp_CODEMC/nuevo_curso.html", ctx)