from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Transaction
from sales.models import Sale, Customer

User = get_user_model()

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='finance@test.com', password='password')
        self.customer = Customer.objects.create(name='Finance Customer')
        self.sale = Sale.objects.create(customer=self.customer, seller=self.user)
        
        self.transaction = Transaction.objects.create(
            description='Test Transaction',
            amount=100.00,
            type='INCOME',
            status='PENDING',
            due_date=timezone.now().date(),
            sale=self.sale
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.amount, 100.00)
        self.assertEqual(self.transaction.type, 'INCOME')
        self.assertEqual(self.transaction.sale, self.sale)
        self.assertIn('Test Transaction', str(self.transaction))

    def test_transaction_status_update(self):
        self.transaction.status = 'PAID'
        self.transaction.paid_date = timezone.now().date()
        self.transaction.save()
        self.assertEqual(self.transaction.status, 'PAID')
        self.assertIsNotNone(self.transaction.paid_date)

class FinanceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(email='admin@example.com', password='password', role='ADMIN')
        self.seller = User.objects.create_user(email='seller@example.com', password='password', role='SELLER')
        self.client = Client()

    def test_seller_cannot_delete_transaction(self):
        # Transaction deletion is admin-only
        tx = Transaction.objects.create(
            description='Servidor Cloud',
            amount=150.00,
            type='EXPENSE',
            status='PENDING',
            due_date=timezone.now().date()
        )
        self.client.login(email='seller@example.com', password='password')
        response = self.client.post(reverse('transaction_delete', args=[tx.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(pk=tx.pk).exists())

    def test_admin_can_delete_transaction(self):
        tx = Transaction.objects.create(
            description='Material Escritório',
            amount=50.00,
            type='EXPENSE',
            status='PENDING',
            due_date=timezone.now().date()
        )
        self.client.login(email='admin@example.com', password='password')
        response = self.client.post(reverse('transaction_delete', args=[tx.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(pk=tx.pk).exists())

    def test_create_income_transaction(self):
        tx = Transaction.objects.create(
            description='Consultoria Avulsa',
            amount=500.00,
            type='INCOME',
            status='PAID',
            due_date=timezone.now().date(),
            paid_date=timezone.now().date()
        )
        self.assertEqual(str(tx), 'Consultoria Avulsa - 500.0')
