from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Reserva, Cliente
import re
from django.utils import timezone

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["fecha_inicio", "fecha_fin"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        hoy = timezone.localdate()  # fecha actual del sistema

        if fecha_inicio and fecha_fin:
            if fecha_inicio < hoy:
                raise forms.ValidationError("⚠️ No puedes reservar fechas en el pasado.")
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError("⚠️ La fecha de término no puede ser anterior a la de inicio.")
        return cleaned_data


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    rut_pasaporte = forms.CharField(max_length=20)
    telefono = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2",
            "nombre", "apellido", "rut_pasaporte", "telefono"
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_rut_pasaporte(self):
        rut = self.cleaned_data.get("rut_pasaporte")
        if not re.match(r'^[0-9]+-[0-9kK]{1}$', rut):
            raise forms.ValidationError("El RUT debe tener el formato 12345678-9")
        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números.")
        return telefono

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            group, _ = Group.objects.get_or_create(name="Clientes")
            user.groups.add(group)
            Cliente.objects.create(
                user=user,
                nombre=self.cleaned_data["nombre"],
                apellido=self.cleaned_data["apellido"],
                rut_pasaporte=self.cleaned_data["rut_pasaporte"],
                email=self.cleaned_data["email"],
                telefono=self.cleaned_data["telefono"]
            )
        return user
