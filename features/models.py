from django.db import models

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length = 200)
    logo = models.ImageField(upload_to='logos/')
    qr_logo = models.ImageField(upload_to='qr_logos/')
    facebook_url = models.CharField(max_length = 200, null=True, blank=True)
    instagram_url = models.CharField(max_length = 200, null=True, blank=True)
    youtube_url = models.CharField(max_length = 200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)