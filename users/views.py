from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        send_mail(
            'Добро пожаловать!',
            'Вы успешно зарегистрировались на нашем сайте.',
            settings.DEFAULT_FROM_EMAIL,
            [self.object.email],
            fail_silently=False,
        )
        return response

