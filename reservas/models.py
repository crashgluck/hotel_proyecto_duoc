from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut_pasaporte = models.CharField(max_length=20, unique=True)  # agregado
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Habitacion(models.Model):
    CATEGORIAS = [
        ('TURISTA', 'Turista'),
        ('PREMIUM', 'Premium'),
    ]

    numero = models.IntegerField(unique=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    descripcion = models.TextField()
    equipamiento = models.TextField(blank=True, null=True)  # agregado
    precio_diario = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"Habitación {self.numero} - {self.categoria}"


class ImagenHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='habitaciones/')  # soporta mínimo 3 imágenes por habitación

    def __str__(self):
        return f"Imagen de Habitación {self.habitacion.numero}"


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    confirmada = models.BooleanField(default=False)
    monto_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # agregado
    monto_reserva = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # agregado

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente}"


class Pago(models.Model):
    METODOS = [
        ('TARJETA', 'Tarjeta de crédito/débito'),
        ('TRANSFERENCIA', 'Transferencia bancaria'),
        ('EFECTIVO', 'Efectivo'),
    ]

    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=8, decimal_places=2)
    monto_reserva = models.DecimalField(max_digits=8, decimal_places=2)
    metodo = models.CharField(max_length=20, choices=METODOS)  # agregado
    fecha_pago = models.DateTimeField(auto_now_add=True)
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pago de Reserva {self.reserva.id}"
