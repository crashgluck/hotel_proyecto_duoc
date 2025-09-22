from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Reserva, Cliente

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["fecha_inicio", "fecha_fin"]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    rut_pasaporte = forms.CharField(max_length=20)
    telefono = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "nombre", "apellido", "rut_pasaporte", "telefono")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # ➝ Asignar al grupo "Clientes"
            clientes_group, created = Group.objects.get_or_create(name="Clientes")
            user.groups.add(clientes_group)

            # ➝ Crear registro en Cliente
            Cliente.objects.create(
                user=user,
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                rut_pasaporte=self.cleaned_data['rut_pasaporte'],
                email=self.cleaned_data['email'],
                telefono=self.cleaned_data['telefono']
            )
        return user