from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.db import connection
import bcrypt


from . import forms
# Create your views here.
def index(request):
    ctx = {}
    return render(request,'miapp_CODEMC/index.html',ctx)


def planes(request):
    return render(request,"miapp_CODEMC/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/Contacto.html")

def inicio_usuario(request):
    if request.method == 'POST':
        form = forms.FormularioLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data["gmail"]
            contraseña = form.cleaned_data["contraseña"]
            #Verifica si el usuario existe y la contraseña es correcta

            with connection.cursor() as cursor:
                # Obtén el hash de la contraseña almacenado
                cursor.execute("SELECT contraseña FROM usuarios WHERE email = %s", [email])
                cursor= cursor.fetchone()

                if cursor:
                    stored_hash = cursor[0]

                    # Verifica la contraseña
                    if bcrypt.checkpw(contraseña.encode('utf-8'), stored_hash.encode('utf-8')):
                        return HttpResponse("Inicio de sesión exitoso")
                    else:
                        return HttpResponse("Contraseña incorrecta")
                else:
                    return HttpResponse("Usuario no encontrado")
           
    else:
        form = forms.FormularioLogin()
    ctx = {"form":form}
    return render(request, "miapp_CODEMC/Inicio_login.html",ctx)


def inicio_registro(request):
    if request.method == 'POST':
        form = forms.FormularioRegistro(request.POST)
        if form.is_valid():
            email = form.cleaned_data["gmail"]
            contraseña = form.cleaned_data["contraseña"]
            validar_contraseña = form.cleaned_data["validar_contraseña"]
            if contraseña != validar_contraseña:
                return HttpResponse("Las contraseñas no coinciden.")

            # Validar si el email ya está registrado
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s", [email])
                email_count = cursor.fetchone()[0]

            if email_count > 0:
                return HttpResponse("Este correo electrónico ya está registrado.")

            # Insertar el nuevo usuario en la base de datos
            hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO usuarios (email, contraseña) VALUES (%s, %s)", [email, hashed])

            return redirect('login')  # Redirige a la página de inicio de sesión o a otra página
    else:
        form = forms.FormularioRegistro()
    ctx = {"form":form}
    return render(request, "miapp_CODEMC/inicio_registro.html", ctx)

