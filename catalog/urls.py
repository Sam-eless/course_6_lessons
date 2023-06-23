from django.views.decorators.cache import cache_page
from catalog.apps import CatalogConfig
from django.urls import path

from catalog.views import home, contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    # path('products/', cache_page(60)(ProductListView.as_view()), name='products'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('create/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_item'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_item'),
]
