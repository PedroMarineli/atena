from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventory.models import Product, Supplier
from sales.models import Sale, SaleItem, Customer
from finance.models import Transaction

User = get_user_model()

class SaleFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client = Client()
        self.client.login(email='test@example.com', password='password')
        
        self.customer = Customer.objects.create(name='Test Customer')
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST-SKU',
            price=100.00,
            stock=10,
            supplier=self.supplier
        )
        self.sale = Sale.objects.create(customer=self.customer, seller=self.user)

    def test_add_item_stock_check(self):
        # Try to add more than stock
        response = self.client.post(reverse('sale_add_item', args=[self.sale.pk]), {
            'product': self.product.pk,
            'quantity': 11
        }, follow=True)
        
        messages = list(response.context['messages'])
        self.assertTrue(any('Estoque insuficiente' in str(m) for m in messages))
        self.assertEqual(self.sale.items.count(), 0)

    def test_finalize_sale(self):
        # Add item
        SaleItem.objects.create(sale=self.sale, product=self.product, quantity=5, price=100.00)
        self.sale.total = 500.00
        self.sale.save()
        
        # Finalize
        response = self.client.post(reverse('sale_finalize', args=[self.sale.pk]), follow=True)
        
        self.sale.refresh_from_db()
        self.product.refresh_from_db()
        
        self.assertEqual(self.sale.status, 'COMPLETED')
        self.assertEqual(self.product.stock, 5) # 10 - 5
        
        # Check transaction
        transaction = Transaction.objects.get(sale=self.sale)
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.type, 'INCOME')

    def test_finalize_sale_insufficient_stock(self):
        # Add item
        SaleItem.objects.create(sale=self.sale, product=self.product, quantity=5, price=100.00)
        self.sale.total = 500.00
        self.sale.save()
        
        # Change stock to be insufficient
        self.product.stock = 4
        self.product.save()
        
        # Finalize
        response = self.client.post(reverse('sale_finalize', args=[self.sale.pk]), follow=True)
        
        self.sale.refresh_from_db()
        self.product.refresh_from_db()
        
        self.assertEqual(self.sale.status, 'PENDING')
        self.assertEqual(self.product.stock, 4) # Unchanged
        
        messages = list(response.context['messages'])
        self.assertTrue(any('Estoque insuficiente' in str(m) for m in messages))
