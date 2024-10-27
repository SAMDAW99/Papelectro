from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from .forms import LoginForm
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'main/home.html'


class UserLoginView(LoginView):
    form_class = LoginForm  
    template_name = 'main/login.html'

    def get_success_url(self):
        # Redirecciona al dashboard adecuado según el rol del usuario
        if self.request.user.is_superuser:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('user_dashboard')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser
    

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/user_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return super().dispatch(request, *args, **kwargs)
