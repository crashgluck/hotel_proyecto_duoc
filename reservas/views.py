from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Habitacion, Reserva, Cliente
from .forms import ReservaForm, RegistroForm


def es_cliente(user):
    return user.groups.filter(name="Clientes").exists()

def landing(request):
    # Enviar un mensaje informativo
    messages.info(request, 'Todas las reservas son con un pago anticipado del 30% del monto total.')

    # Puedes enviar otros tipos de mensajes, por ejemplo:
    # messages.success(request, 'Reserva confirmada correctamente.')
    # messages.error(request, 'Hubo un error en tu reserva.')
    return render(request, "reservas/landing.html")

def ver_habitaciones(request):

    messages.info(request, 'Busca las habitaciones disponibles en las fechas que deseas.')
    fecha_inicio    = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    habitaciones = Habitacion.objects.none()  # por defecto no trae nada

    if fecha_inicio and fecha_fin:
        # Solo buscar si el usuario envió fechas
        habitaciones = Habitacion.objects.all().prefetch_related("imagenes")

        # Excluir habitaciones ocupadas en esas fechas
        habitaciones = habitaciones.exclude(
            reserva__fecha_inicio__lte=fecha_fin,
            reserva__fecha_fin__gte=fecha_inicio
        )

    return render(request, "reservas/habitaciones.html", {
        "habitaciones": habitaciones,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })

@login_required
def realizar_reserva(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)
    cliente = get_object_or_404(Cliente, email=request.user.email)

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.habitacion = habitacion
            reserva.cliente = cliente

            # --- Validar traslape ---
            if reserva.overlaps():
                form.add_error(None, "⚠️ La habitación ya está reservada en esas fechas.")
            else:
                # Calcular monto
                dias = (reserva.fecha_fin - reserva.fecha_inicio).days + 1
                reserva.monto_total = dias * habitacion.precio_diario
                reserva.monto_reserva = int(reserva.monto_total * 0.3)
                reserva.save()
                return redirect("mis_reservas")
    else:
        form = ReservaForm()

    return render(request, "reservas/reserva_form.html", {"form": form, "habitacion": habitacion})

@login_required
def mis_reservas(request):
    cliente = get_object_or_404(Cliente, email=request.user.email)
    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, "reservas/mis_reservas.html", {"reservas": reservas})

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("landing")
    else:
        form = RegistroForm()
    return render(request, "reservas/registro.html", {"form": form})


@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, cliente__email=request.user.email)

    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)

            # --- Validar traslape excluyendo la reserva actual ---
            if Reserva.objects.filter(
                habitacion=nueva_reserva.habitacion,
                fecha_inicio__lte=nueva_reserva.fecha_fin,
                fecha_fin__gte=nueva_reserva.fecha_inicio
            ).exclude(id=reserva.id).exists():
                form.add_error(None, "⚠️ La habitación ya está reservada en esas fechas.")
            else:
                # Recalcular monto
                dias = (nueva_reserva.fecha_fin - nueva_reserva.fecha_inicio).days + 1
                nueva_reserva.monto_total = dias * reserva.habitacion.precio_diario
                nueva_reserva.monto_reserva = int(nueva_reserva.monto_total * 0.3)
                nueva_reserva.save()

                messages.success(request, "✅ Reserva actualizada con éxito.")
                return redirect("mis_reservas")
    else:
        form = ReservaForm(instance=reserva)

    return render(request, "reservas/editar_reserva.html", {
        "form": form,
        "reserva": reserva
    })