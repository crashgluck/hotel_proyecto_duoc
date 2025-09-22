from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('habitaciones/', views.ver_habitaciones, name='ver_habitaciones'),
    path('reservar/<int:habitacion_id>/', views.realizar_reserva, name='realizar_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('registro/', views.registro, name='registro'),
    path('reservas/<int:reserva_id>/editar/', views.editar_reserva, name='editar_reserva'),
]
