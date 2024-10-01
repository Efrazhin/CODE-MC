from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib import messages

from .forms import *

# Create your views here.
def index(request):
    ctx = {}
    return render(request, 'miapp_CODEMC/index.html', ctx)

def planes(request):
    return render(request, "miapp_CODEMC/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/Contacto.html")

def inicio_gestion(request):
    return render(request, "miapp_codemc/inicio_gestion.html")

def sucursales(request):
    return render(request, "miapp_codemc/sucursales.html")

def estadisticas(request):
    return render(request, "miapp_codemc/estadisticas.html")

def inicio_usuario(request):
    if request.method == 'POST':
        form = forms.FormularioLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data["gmail"]
            contraseña = form.cleaned_data["contraseña"]
            # Verifica si el usuario existe y la contraseña es correcta

            with connection.cursor() as cursor:
                # Obtén la contraseña almacenada en texto plano
                cursor.execute("SELECT contraseña FROM usuarios WHERE email = %s", [email])
                cursor = cursor.fetchone()

                if cursor:
                    stored_password = cursor[0]

                    # Verifica la contraseña en texto plano
                    if contraseña == stored_password:
                        return redirect("inicio gestion")
                    else:
                        messages.error(request, "Contraseña incorrecta. Inténtalo de nuevo.")
                else:
                    messages.error(request, "Usuario no encontrado.")
    else:
        form = forms.FormularioLogin()
    ctx = {"form": form}
    return render(request, "miapp_CODEMC/Inicio_login.html", ctx)

def inicio_registro(request):
    if request.method == 'POST':
        form = forms.FormularioRegistroEmpresa(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Codigo de mierda")
    else:
        form = forms.FormularioRegistroEmpresa()
    ctx = {"form": form}
    return render(request, "miapp_CODEMC/inicio_registro.html", ctx)


