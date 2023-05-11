from catalog.models import Product
from django.shortcuts import render
from django.http import HttpResponse


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


def products(request):
    context = {
        'products_list': Product.objects.all(),
        'title': 'Список продуктов'
    }
    return render(request, 'products.html', context)


def product(request, pk):
    product_item = Product.objects.get(pk=pk)
    context = {
        'object': product_item,
        'title': product_item.name
    }
    return render(request, 'product.html', context)
