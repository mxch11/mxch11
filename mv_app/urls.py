from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.landing_page, name='landing_page'),
    path('p_inicio/', views.p_inicio, name='p_inicio'),
    path('d_inicio/', views.d_inicio, name='d_inicio'),
    path('u_inicio/', views.p_inicio, name='u_inicio'),
]