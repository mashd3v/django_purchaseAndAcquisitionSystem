from django.urls import path, include
from .views import ProductList, ProductDetail

urlpatterns = [
    path('v1/products/', ProductList.as_view(), name='productList'),
    path('v1/products/<str:code>', ProductDetail.as_view(), name='productDetail'),
]