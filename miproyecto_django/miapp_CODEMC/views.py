from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def index(request):
    contexto_random = {}
    return render(request,'miapp_CODEMC/index.html',contexto_random)