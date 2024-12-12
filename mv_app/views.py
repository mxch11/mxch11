from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .models import Reserva
from .models import Servicio
from .models import Estilista
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def landing_page(request):
    return render(request, 'landing_page.html')

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
def p_inicio(request):
    estilistas = Estilista.objects.all() # Filtra según sea necesario
    servicios = Servicio.objects.filter(categoria = 'pestañas')
    return render(request, 'servicios/pestañas/inicio.html', {'estilistas': estilistas, 'servicios': servicios})

@login_required
def d_inicio(request):

    estilistas = Estilista.objects.all() # Filtra según sea necesario
    servicios = Servicio.objects.filter(categoria = 'depilacion')
    return render(request, 'servicios/depilacion/inicio.html', {'estilistas': estilistas, 'servicios': servicios})


@login_required
def u_inicio(request):
    estilistas = Estilista.objects.all() # Filtra según sea necesario
    servicios = Servicio.objects.filter(categoria = 'uñas')
    return render(request, 'servicios/uñas/inicio.html', {'estilistas': estilistas, 'servicios': servicios})

meses_es_en = {
    'Enero': 'January', 'Febrero': 'February', 'Marzo': 'March',
    'Abril': 'April', 'Mayo': 'May', 'Junio': 'June',
    'Julio': 'July', 'Agosto': 'August', 'Septiembre': 'September',
    'Octubre': 'October', 'Noviembre': 'November', 'Diciembre': 'December'
}

def convertir_fecha(fecha):
    for mes_es, mes_en in meses_es_en.items():
        if mes_es in fecha:
            fecha = fecha.replace(mes_es, mes_en)
            break
    return datetime.strptime(fecha, '%d %B %Y').date()
@login_required
def reservar_hora(request):
    if request.method == 'POST':
        # Obtener los IDs enviados
        servicio_id = request.POST.get('servicio_id')
        profesional_id = request.POST.get('profesional_id')
        fecha = request.POST.get('fecha')

        try:
            fecha_obj = convertir_fecha(fecha)
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha invalido. Debe ser como "28 Noviembre 2024".'}, status=400)


        try:
            servicio = Servicio.objects.get(id=servicio_id[0])
            profesional = Estilista.objects.get(id=profesional_id)
        except (Servicio.DoesNotExist, Estilista.DoesNotExist) as e:
            return JsonResponse({'error': 'Servicio o profesional no encontrado'}, status=404)


        reserva_ = Reserva.objects.create(
            servicio = servicio,
            estilista = profesional,
            fecha = fecha_obj,
            hora = '14:30',
            usuario=request.user
        )

        # Procesar los datos (buscar objetos en la base de datos, etc.)
        print(f"Servicio ID: {servicio_id}, Profesional ID: {profesional_id}, Fecha: {fecha_obj}")


        return render(request, 'confirmacion.html', {
            'servicio': servicio.nombre,
            'profesional': profesional.nombre,
            'fecha': fecha_obj.strftime('%d/%m/%Y'),
            'usuario': request.user.username,
        })

    # Si el método no es POST, redirige al inicio o muestra un error
    return JsonResponse({'error': 'Método no permitido'}, status=405)



@login_required
def mis_reservas(request):
    # Obtener las reservas del usuario autenticado
    if request.user.is_staff:  # Si el usuario tiene acceso al panel de administración
        reservas = Reserva.objects.all().order_by('-fecha', '-hora')
    else:
        reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha', '-hora')
    

    return render(request, 'servicios/reservas/mis_reservas.html', {'reservas': reservas})

@login_required
def cancelar_reserva(request, reserva_id):
    if request.method == 'POST':
        # Obtener la reserva y validar que pertenece al usuario
        if request.user.is_staff:  # Si el usuario tiene acceso al panel de administración
            reserva = get_object_or_404(Reserva, id=reserva_id)

        else:
            reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

        # Validar si la reserva es cancelable
        if not reserva.es_cancelable():
            messages.error(request, 'La reserva no puede ser cancelada porque faltan menos de 3 días.')
            return redirect('mis_reservas')

        # Eliminar la reserva
        reserva.delete()
        messages.success(request, 'Reserva cancelada correctamente.')
        return redirect('mis_reservas')

    return redirect('mis_reservas')  # Redirige si el método no es POST