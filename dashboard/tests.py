from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Organization

User = get_user_model()

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='dashboard@test.com', password='password')
        self.client = Client()

    def test_dashboard_redirects_anonymous(self):
        response = self.client.get(reverse('index'))
        self.assertNotEqual(response.status_code, 200)
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_dashboard_access_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

class DashboardTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email='admin@example.com', password='password')
        self.seller = User.objects.create_user(email='seller@example.com', password='password', role='SELLER')
        self.client = Client()

    def test_organization_singleton(self):
        org1 = Organization.load()
        org1.name = "Atena Comércio"
        org1.save()

        org2 = Organization.load()
        self.assertEqual(org2.name, "Atena Comércio")
        self.assertEqual(org1.pk, 1)
        self.assertEqual(org2.pk, 1)

    def test_superuser_creation(self):
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)
        self.assertEqual(self.admin.role, 'ADMIN')

    def test_seller_cannot_access_user_list(self):
        self.client.login(email='seller@example.com', password='password')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_access_user_list(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_charts_endpoint(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.get(reverse('dashboard_charts_data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('sales_chart', data)
        self.assertIn('cash_flow_chart', data)
        self.assertIn('top_products_chart', data)
        self.assertIn('mix_chart', data)
