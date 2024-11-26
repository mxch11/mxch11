from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    path('p_inicio/', views.p_inicio, name='p_inicio'),
    path('d_inicio/', views.d_inicio, name='d_inicio'),
    path('u_inicio/', views.u_inicio, name='u_inicio'),
    path('reservar/', views.reservar_hora, name='reservar_hora'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('accounts/register/', views.register, name='register'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]