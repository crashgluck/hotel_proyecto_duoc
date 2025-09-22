from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'reservas/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name="Administradores").exists():
            return reverse_lazy('reservas_list_admin')   # Panel admin
        elif user.groups.filter(name="Clientes").exists():
            return reverse_lazy('mis_reservas')          # Catálogo o reservas
        else:
            return reverse_lazy('mis_reservas')                  # Página por defecto
