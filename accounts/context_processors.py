from features.models import *
from django.template.context_processors import request

def custom_data(request):
    company = Company.objects.all().order_by('-created').first()
    return {'company': company}

    