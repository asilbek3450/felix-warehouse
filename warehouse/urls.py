from django.urls import path
from .views import ProductMaterialListView, WarehouseListView, get_materials_view

urlpatterns = [
    path('productmaterial/', ProductMaterialListView.as_view()),
    path('warehouse/', WarehouseListView.as_view()),
    path('get_materials/', get_materials_view, name='get_materials'),
]

