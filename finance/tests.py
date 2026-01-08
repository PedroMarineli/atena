from django.test import TestCase
from finance.models import Transaction
from sales.models import Sale, Customer
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

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
