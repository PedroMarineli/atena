from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from .models import Supplier, Product, Service

User = get_user_model()

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
        with self.assertRaises(Exception):
            Product.objects.create(
                name='Another Product',
                sku='TEST-Product-001',
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

class InventoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='inventory_user@example.com', password='password', role='ADMIN')
        self.client = Client()
        self.client.login(email='inventory_user@example.com', password='password')

        self.supplier = Supplier.objects.create(
            name='Distribuidora Alpha',
            email='contato@alpha.com',
            phone='11999998888',
            document='12.345.678/0001-90',
            contact_name='Carlos'
        )

    def test_create_product(self):
        product = Product.objects.create(
            name='Parafuso 6mm',
            sku='PAR-001',
            price=1.50,
            cost_price=0.50,
            stock=100,
            min_stock=20,
            unit='UN',
            supplier=self.supplier
        )
        self.assertEqual(str(product), 'Parafuso 6mm (PAR-001)')
        self.assertEqual(product.supplier.name, 'Distribuidora Alpha')

    def test_create_service(self):
        service = Service.objects.create(
            name='Consultoria Técnica',
            price=250.00,
            supplier=self.supplier
        )
        self.assertEqual(str(service), 'Consultoria Técnica')

    def test_supplier_delete_sets_null_on_product(self):
        product = Product.objects.create(
            name='Produto Teste',
            sku='PROD-TEST',
            price=10.00,
            stock=5,
            supplier=self.supplier
        )
        response = self.client.post(reverse('supplier_delete', args=[self.supplier.pk]), follow=True)
        self.assertFalse(Supplier.objects.filter(pk=self.supplier.pk).exists())
        product.refresh_from_db()
        self.assertIsNone(product.supplier)

    def test_product_protected_when_sale_item_exists(self):
        from sales.models import Customer, Sale, SaleItem
        customer = Customer.objects.create(name='Cliente Teste')
        sale = Sale.objects.create(customer=customer, seller=self.user)
        product = Product.objects.create(
            name='Produto Protegido',
            sku='PROD-PROT',
            price=20.00,
            stock=10
        )
        SaleItem.objects.create(sale=sale, product=product, quantity=2, price=20.00)

        response = self.client.post(reverse('item_delete', args=[product.pk]), follow=True)
        self.assertTrue(Product.objects.filter(pk=product.pk).exists())
        messages = list(response.context['messages'])
        self.assertTrue(any('Não é possível excluir este produto' in str(m) for m in messages))
