from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer
from inventario.models import Product
from django.db.models import Q

class ProductList(APIView):
    def get(self, request):
        product = Product.objects.all()
        data = ProductSerializer(product, many=True).data
        return Response(data)

class ProductDetail(APIView):
    def get(self, request, code):
        product = get_object_or_404(Product, Q(code=code)|Q(barCode=code))
        data = ProductSerializer(product).data
        return Response(data)
