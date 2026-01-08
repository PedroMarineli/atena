from django.test import TestCase
from inventory.models import Supplier, Product
from django.core.exceptions import ValidationError

class SupplierModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='supplier@example.com',
            phone='1234567890',
            document='12345678000199',
            contact_name='Contact Person'
        )

    def test_supplier_creation(self):
        self.assertEqual(self.supplier.name, 'Test Supplier')
        self.assertEqual(str(self.supplier), 'Test Supplier')

class ProductModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name='Supplier for Product')
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST-Product-001',
            price=50.00,
            cost_price=30.00,
            stock=100,
            min_stock=10,
            unit='UN',
            supplier=self.supplier
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.stock, 100)
        self.assertEqual(str(self.product), 'Test Product (TEST-Product-001)')

    def test_sku_uniqueness(self):
        with self.assertRaises(Exception): # IntegrityError usually, but strict Exception catch for simplicity in basic test
            Product.objects.create(
                name='Another Product',
                sku='TEST-Product-001', # Same SKU
                price=20.00
            )

    def test_default_values(self):
        product_minimal = Product.objects.create(
            name='Minimal Product',
            sku='MIN-001',
            price=10.00
        )
        self.assertEqual(product_minimal.stock, 0)
        self.assertEqual(product_minimal.unit, 'UN')
