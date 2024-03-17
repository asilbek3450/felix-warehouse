from rest_framework import serializers

from .models import ProductMaterial, Warehouse, Material, Product


class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = ['id', 'product_id', 'material_id', 'quantity_material', 'unit']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'material_id', 'remainder', 'price', 'date']

    def validate(self, data):
        remainder = data.get('remainder', None)
        price = data.get('price', None)

        if remainder < 0:
            raise ValueError(
                {
                    'status': False,
                    'message': "Qolgan xomashyo miqdori manfiy bo'lishi mumkin emas"
                }
            )

        if price < 0:
            raise ValueError({'status': False, 'message': "Narx manfiy bo'lishi mumkin emas"})

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['date'] = instance.date.strftime('%d-%m-%Y')
        return response


