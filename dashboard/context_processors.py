from .models import Organization

def organization(request):
    return {'organization': Organization.load()}
