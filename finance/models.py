from django.db import models
from sales.models import Sale

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('INCOME', 'Receita'),
        ('EXPENSE', 'Despesa'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago'),
    ]
    
    description = models.CharField(max_length=255, verbose_name="Descrição")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Tipo")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    paid_date = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento")
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions', verbose_name="Venda")
    
    def __str__(self):
        return f"{self.description} - {self.amount}"
