from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_liveness_probe_returns_200(self):
        """Liveness endpoint should return 200 OK and healthy status."""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'healthy')
        self.assertEqual(data.get('probe'), 'liveness')

    def test_readiness_probe_success(self):
        """Readiness endpoint should return 200 OK when database is accessible."""
        response = self.client.get('/ready')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'ready')
        self.assertEqual(data.get('database'), 'connected')

    @patch('django.db.connection.cursor')
    def test_readiness_probe_failure_returns_503(self, mock_cursor):
        """Readiness endpoint should return 503 Service Unavailable if database check fails."""
        mock_cursor.side_effect = Exception("DB Connection refused")
        response = self.client.get('/ready')
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data.get('status'), 'unhealthy')
        self.assertEqual(data.get('database'), 'disconnected')
