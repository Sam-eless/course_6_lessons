from catalog.models import Product
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Получено сообщение от пользователя {name} (телефон: {phone}): {message}')
    return render(request, 'contacts.html')


def products(request):
    context = {
        'products_list': Product.objects.all(),
        'title': 'Список продуктов'
    }
    return render(request, 'products.html', context)