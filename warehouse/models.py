from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    
class ProductMaterial(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_material = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=255)  # kg, l, m3, m2, m1, etc.

    def __str__(self):
        return self.product_id.name + " uchun " + str(self.quantity_material) + " " + str(self.unit) + " " + self.material_id.name + " kerak"


class Warehouse(models.Model):
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.IntegerField()  # qolgan xomashyo miqdori
    price = models.DecimalField(max_digits=20, decimal_places=2)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.material_id.name + " " + str(self.remainder)

