from PIL.ImageQt import _toqclass_helper
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory

from catalog.forms import ProductForm, VersionForm, ProductFormModer
from catalog.models import Product, Version
from django.shortcuts import render
from django.urls import reverse_lazy

from django.http import HttpResponse, request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.services.cache_list_categories import get_all_categories


# Create your views here.

def home(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Получено сообщение от пользователя {name} (телефон: {phone}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'contacts.html', context)


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        context_data['versions'] = Version.objects.filter(product=self.object, is_active=True)
        context_data['category_list'] = get_all_categories()
        return context_data


class ProductListView(ListView):
    model = Product
    context_object_name = 'products_list'
    extra_context = {
        'title': 'Товары'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("can_unpublish_product") and self.request.user.is_authenticated:
            return queryset
        else:
            queryset = queryset.filter(is_published=True)
            return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    # fields = ('name', 'description', 'category', 'purchase_price')
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_create')
    extra_context = {
        'title': 'Добавить продукт'
    }

    def form_valid(self, form):
        form.instance.author = self.request.user if self.request.user.is_authenticated else None
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # PermissionRequiredMixin - пока убрал
    model = Product
    # fields = ('name', 'description', 'category', 'purchase_price',)
    form_class = ProductForm
    template_name = "catalog/product_form_with_formset.html"
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Редактирование'
    }

    def test_func(self):
        product = self.get_object()
        moderator = self.request.user.has_perm(
            "catalog.can_change_description_any_product") and self.request.user.has_perm(
            'catalog.can_change_category_any_product')
        if moderator:
            return True
        else:
            return self.request.user == product.author

    # def test_func(self):
    #     product = self.get_object()
    #     return self.request.user == product.author

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь автором этого продукта.")

    def get_form_class(self, ):
        class_form = ProductFormModer
        if not self.request.user.has_perm('catalog.can_change_description_any_product'):
            class_form = ProductForm
        return class_form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


#
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        product = self.get_object()
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return True
        else:
            return self.request.user == product.author

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь автором этого продукта.")
