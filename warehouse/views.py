from django.http import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from decimal import Decimal

from .serializers import ProductMaterialSerializer, WarehouseSerializer
from .models import ProductMaterial, Warehouse, Material, Product


class ProductMaterialListView(APIView):

    def get(self, request, *args, **kwargs):
        data = {
            'message': 'Success',
            'count': ProductMaterial.objects.count(),
            'result': ProductMaterialSerializer(ProductMaterial.objects.all(), many=True).data
        }
        return Response(data)


class WarehouseListView(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


def get_materials_from_warehouse(request):
    result = []

    # Iterate over each product and its quantity in the request
    for product_name, product_qty in request.items():
        product_materials = []
        product = {
            "product_name": product_name,
            "product_qty": product_qty,
            "product_materials": product_materials
        }

        # Dictionary to keep track of remaining quantity needed for each material
        remaining_material_qty = defaultdict(Decimal)

        # Fetch all materials needed for the product
        product_material_objs = ProductMaterial.objects.filter(product_id__name=product_name)

        # Iterate over each material required for the product
        for product_material_obj in product_material_objs:
            material_name = product_material_obj.material_id.name
            material_qty_needed = Decimal(product_material_obj.quantity_material) * Decimal(product_qty)

            # Flag to track if the material is fully fulfilled
            material_fulfilled = False

            # Find suitable warehouse batches for the material
            warehouse_batches = Warehouse.objects.filter(material_id__name=material_name).order_by('date')

            # Iterate over warehouse batches to fulfill material requirement
            for batch in warehouse_batches:
                # Check if remaining quantity needed is already fulfilled for this material
                if remaining_material_qty[material_name] >= material_qty_needed:
                    material_fulfilled = True
                    break

                # Calculate available material quantity in the batch, for next product_material_obj it should decrease
                available_qty = batch.remainder - remaining_material_qty[material_name]

                # Check if available quantity is sufficient to fulfill the requirement
                if available_qty > 0:
                    # Calculate how much quantity can be taken from this batch
                    quantity_to_take = min(available_qty, material_qty_needed - remaining_material_qty[material_name])

                    # Add the material from this batch to the result
                    product_materials.append({
                        "warehouse_id": batch.id,
                        "material_name": material_name,
                        "qty": quantity_to_take,
                        "price": batch.price
                    })

                    # Update remaining quantity needed for this material
                    remaining_material_qty[material_name] += quantity_to_take

                    # Check if all required quantity for this material has been fulfilled
                    if remaining_material_qty[material_name] >= material_qty_needed:
                        material_fulfilled = True
                        break

            # If material not fully fulfilled, add null entry
            if not material_fulfilled:
                product_materials.append({
                    "warehouse_id": None,
                    "material_name": material_name,
                    "qty": material_qty_needed - remaining_material_qty[material_name],
                    "price": None
                })

        result.append(product)

    return {"result": result}


def get_materials_view(request):
    products_and_quantities = request.GET.dict()
    result = get_materials_from_warehouse(products_and_quantities)
    return JsonResponse(result)
