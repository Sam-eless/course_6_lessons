from catalog.models import Product
from django.shortcuts import render
from django.http import HttpResponse
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

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['title'] = 'any'
    #     return context_data


# def products(request):
#     context = {
#         'products_list': Product.objects.all(),
#         'title': 'Список продуктов'
#     }
#     return render(request, 'products.html', context)


class ProductListView(ListView):
    model = Product
    context_object_name = 'products_list'
    extra_context = {
        'title': 'Товары'
    }
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['title'] = 'Товары'
    #     return context_data

# def product(request, pk):
#     product_item = Product.objects.get(pk=pk)
#     context = {
#         'object': product_item,
#         'title': product_item.name
#     }
#     return render(request, 'product_detail.html', context)






