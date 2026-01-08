from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

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
        if response.status_code != 200:
            print(f"Status: {response.status_code}")
            print(f"Content: {response.content.decode('utf-8')}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
