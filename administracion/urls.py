from django.urls import path
from . import views

urlpatterns = [
    path('reservas/', views.reservas_list, name='reservas_list_admin'),
    path('reservas/<int:pk>/aprobar/', views.aprobar_reserva, name='aprobar_reserva'),
    path('reservas/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]
