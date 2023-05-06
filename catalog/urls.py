from catalog.apps import CatalogConfig
from django.urls import path

from catalog.views import home, contacts, products

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('products/', products, name='products'),
]