from django.conf import settings

def system_version(request):
    return {
        'system_version': getattr(settings, 'SYSTEM_VERSION', 'v0.0.0')
    }
