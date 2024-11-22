from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'base.html')

def p_inicio(request):
    return render(request, 'servicios/pestañas/inicio.html')

def d_inicio(request):
    return render(request, 'servicios/depilacion/inicio.html')

def u_inicio(request):
    return render(request, 'servicios/uñas/inicio.html')