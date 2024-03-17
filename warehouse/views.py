from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .serializers import ProductMaterialSerializer, WarehouseSerializer
from .models import ProductMaterial, Warehouse, Material, Product


class ProductMaterialListView(generics.ListAPIView):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer


class WarehouseListView(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

