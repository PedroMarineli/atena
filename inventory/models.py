from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    TYPE_CHOICES = [
        ('PRODUCT', 'Produto'),
        ('SERVICE', 'Serviço'),
    ]
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='PRODUCT')
    sku = models.CharField(max_length=50, blank=True, null=True) # Required for PRODUCT in logic
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0) # Ignored for SERVICE
    description = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')

    def __str__(self):
        return self.name
