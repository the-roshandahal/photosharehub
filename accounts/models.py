from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    activation_key = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.activation_key:
            self.activation_key = str(uuid.uuid4())
        return super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
