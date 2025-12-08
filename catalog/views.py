from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from config import settings
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category
from django.views.generic import ListView
from django.core.cache import cache

import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        if settings.CACHE_ENABLED:
            key = 'product_list'
            product_list = cache.get(key)
            if not product_list:
                logger.info("Cache miss for product_list, fetching from DB")
                product_list = super().get_queryset()
                cache.set(key, product_list, 60 * 15)
            else:
                logger.info("Cache hit for product_list")
            return product_list
        return super().get_queryset()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    @method_decorator(cache_page(60 * 15))  # Кеширование на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.groups.filter(name='Модератор продуктов').exists()

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.groups.filter(name='Модератор продуктов').exists()

class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'catalog/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')