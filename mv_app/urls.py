from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('index/', views.index, name='index'),
    path('p_inicio/', views.p_inicio, name='p_inicio'),
    path('d_inicio/', views.d_inicio, name='d_inicio'),
    path('u_inicio/', views.u_inicio, name='u_inicio'),
    path('accounts/register/', views.register, name='register'),
]