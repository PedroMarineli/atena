from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    document = models.CharField(max_length=20, blank=True, null=True, verbose_name="CNPJ")
    contact_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pessoa de Contato")
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
        ('UN', 'Unidade'),
        ('KG', 'Quilo'),
        ('L', 'Litro'),
        ('M', 'Metro'),
    ]

    name = models.CharField(max_length=255, verbose_name="Nome")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Preço de Custo")
    stock = models.IntegerField(default=0, verbose_name="Estoque")
    min_stock = models.IntegerField(default=5, verbose_name="Estoque Mínimo")
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='UN', verbose_name="Unidade")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Fornecedor")

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    estimated_duration = models.DurationField(blank=True, null=True, verbose_name="Duração Estimada")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='services', verbose_name="Fornecedor")

    def __str__(self):
        return self.name
