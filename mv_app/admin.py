from django.contrib import admin
from .models import Estilista, Servicio

@admin.register(Estilista)
class EstilistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'foto')
    list_filter = ('especialidad', 'disponibilidad')  # Filtros laterales
    search_fields = ('nombre', 'correo', 'telefono')  # Barra de búsqueda
    ordering = ('nombre',)  # Orden alfabético por nombre

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'duracion', 'precio')
    search_fields = ('nombre',)
    ordering = ('nombre',)
