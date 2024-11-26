from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Estilista(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")  # Ej. Pestañas, Uñas
    experiencia = models.PositiveIntegerField(verbose_name="Años de experiencia")
    disponibilidad = models.BooleanField(default=True, verbose_name="Disponible")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono de contacto", null=True, blank=True)
    correo = models.EmailField(verbose_name="Correo electrónico", null=True, blank=True)
    foto = models.ImageField(upload_to='estilistas/', verbose_name="Foto", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.nombre
    
class Servicio(models.Model):
    
    CATEGORIAS = [
        ('uñas', 'Uñas'),
        ('pelo', 'Pelo'),
        ('depilacion', 'Depilación'),
        ('pestañas', 'Pestañas'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, verbose_name="Categoría")
    descripcion = models.TextField(verbose_name="Descripción")
    duracion = models.PositiveIntegerField(verbose_name="Duración (minutos)")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")

    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    ESTADOS_CITA = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    ]
    fecha_cita = models.DateTimeField()
    hora_cita = models.TimeField()
    estado_cita = models.CharField(max_length=10, choices=ESTADOS_CITA, default='Pendiente')
    comentarios = models.TextField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas_cliente')
    estilista = models.ForeignKey(Estilista, on_delete=models.CASCADE, related_name='citas_estilista')

    def __str__(self):
        return f"Cita con {self.estilista} - {self.fecha_cita} - {self.estado_cita}"

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estilista = models.ForeignKey('Estilista', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    
    def es_cancelable(self):
        # Calcula si quedan más de 3 días para la reserva
        fecha_hora_reserva = datetime.combine(self.fecha, self.hora)
        return fecha_hora_reserva > datetime.now() + timedelta(days=3)

    def __str__(self):
        return f"Reserva de {self.usuario} con {self.estilista} el {self.fecha} a las {self.hora}"
