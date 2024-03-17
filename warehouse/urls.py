from django.urls import path
from .views import ProductMaterialListView, WarehouseListView

urlpatterns = [
    path('productmaterial/', ProductMaterialListView.as_view()),
    path('warehouse/', WarehouseListView.as_view()),
]
