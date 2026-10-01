"""Health check endpoints for container and Kubernetes liveness/readiness probes."""

from django.http import JsonResponse
from django.db import connection
import logging

logger = logging.getLogger(__name__)


def liveness(request):
    """
    Liveness probe endpoint.
    Returns 200 OK as long as the Python/WSGI process is able to serve requests.
    """
    return JsonResponse(
        {
            "status": "healthy",
            "probe": "liveness"
        },
        status=200
    )


def readiness(request):
    """
    Readiness probe endpoint.
    Verifies that the application is fully ready to accept incoming traffic,
    including an active connection and successful query to the PostgreSQL database.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            if not row or row[0] != 1:
                raise RuntimeError("Invalid response from database connection check.")

        return JsonResponse(
            {
                "status": "ready",
                "probe": "readiness",
                "database": "connected"
            },
            status=200
        )
    except Exception as exc:
        logger.error("Readiness probe check failed: %s", exc, exc_info=True)
        return JsonResponse(
            {
                "status": "unhealthy",
                "probe": "readiness",
                "database": "disconnected",
                "error": str(exc)
            },
            status=503
        )
