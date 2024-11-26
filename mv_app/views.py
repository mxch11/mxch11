from django.shortcuts import render, redirect, get_object_or_404
# from .models import
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'base.html')


def register(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Validar las contraseñas
        if password != password_confirm:

            print("Las contraseñas no coinciden.")

            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        # Validar que el email no esté registrado
        if User.objects.filter(email=email).exists():
            print("El correo electrónico ya está registrado.")
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('register')

        # Crear el usuario
        try:
            user = User.objects.create_user(
                username=email,  # Usar el email como username
                email=email,
                password=password
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(
                request, "Registro exitoso. Puedes iniciar sesión.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error al registrar el usuario: {str(e)}")
            return redirect('register')

    return render(request, 'registration/register.html')


@login_required
def landing_page(request):
    return render(request, 'landing_page.html')


def p_inicio(request):
    return render(request, 'servicios/pestañas/inicio.html')


def d_inicio(request):
    return render(request, 'servicios/depilacion/inicio.html')


def u_inicio(request):
    return render(request, 'servicios/uñas/inicio.html')
