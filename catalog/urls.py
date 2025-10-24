from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),          # Главная страница
    path('contacts/', views.contacts, name='contacts'),  # Страница контактов
]
