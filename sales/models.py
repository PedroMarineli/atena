from django.db import models
from django.core.exceptions import ValidationError
from dashboard.models import User
# from inventory.models import Item

class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    document = models.CharField(max_length=20, blank=True, null=True, verbose_name="CPF/CNPJ")
    address = models.TextField(blank=True, null=True, verbose_name="Endereço")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado")
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('COMPLETED', 'Finalizada'),
        ('CANCELED', 'Cancelada'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales', verbose_name="Cliente")
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales', verbose_name="Vendedor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")

    def __str__(self):
        return f"Sale #{self.id} - {self.customer.name}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    # item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='sale_items')
    product = models.ForeignKey('inventory.Product', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Produto")
    service = models.ForeignKey('inventory.Service', null=True, blank=True, on_delete=models.PROTECT, verbose_name="Serviço")
    quantity = models.IntegerField(default=1, verbose_name="Quantidade")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço") # Price at the moment of sale
    
    def clean(self):
        if self.product and self.service:
            raise ValidationError("A SaleItem cannot be both a Product and a Service.")
        if not self.product and not self.service:
            raise ValidationError("A SaleItem must be either a Product or a Service.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        item_name = self.product.name if self.product else (self.service.name if self.service else "Unknown")
        return f"{self.quantity}x {item_name} in Sale #{self.sale.id}"
