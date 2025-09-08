from django.contrib import admin
from .models import Cliente, Habitacion, Reserva, Pago, ImagenHabitacion

admin.site.register(Cliente)
admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Pago)
admin.site.register(ImagenHabitacion)
