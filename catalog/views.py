from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from django.shortcuts import render
from django.urls import reverse_lazy

from django.http import HttpResponse, request
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


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
        return context_data


class ProductListView(ListView):
    model = Product
    context_object_name = 'products_list'
    extra_context = {
        'title': 'Товары'
    }


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


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    # fields = ('name', 'description', 'category', 'purchase_price',)
    form_class = ProductForm
    template_name = "catalog/product_form_with_formset.html"
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Редактирование'
    }
    permission_required = 'catalog.can_edit_product'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.author

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь автором этого продукта.")

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
class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

    permission_required = 'catalog.can_edit_product'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.author

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь автором этого продукта.")