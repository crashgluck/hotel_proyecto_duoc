from django.shortcuts import render, redirect, get_object_or_404
from reservas.models import Reserva

# Listar todas las reservas
def reservas_list(request):
    reservas = Reserva.objects.all().order_by('-fecha_reserva')
    return render(request, 'administracion/reservas_list.html', {'reservas': reservas})

# Aprobar reserva
def aprobar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.confirmada = True
    reserva.save()
    return redirect('reservas_list_admin')

# Cancelar reserva
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.delete()
    return redirect('reservas_list_admin')
