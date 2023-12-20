from django.contrib.auth.models import User
import os
from django.db import models
from django.utils import timezone
import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.conf import settings


# Create your models here.

def generate_filename(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename, extension = os.path.splitext(filename)
    return f"photos/{timestamp}_{filename}{extension}"

def generate_secret_token():
    return str(uuid.uuid4())

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    location = models.CharField(max_length=100, null=True, blank= True)
    remarks = models.CharField(max_length=100, null=True, blank= True)

    event_credentials = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    secret_token = models.CharField(max_length=255, default=generate_secret_token, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.event_credentials:
            self.event_credentials = str(uuid.uuid4())
        if not self.secret_token:
            self.secret_token = generate_secret_token()
        super(Event, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete associated images
        for folder in self.folder_set.all():
            for photo in Photo.objects.filter(folder=folder):
                image_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))
                if os.path.exists(image_path):
                    os.remove(image_path)
                photo.delete()
            folder.delete()

        # Call the superclass delete method
        super(Event, self).delete(*args, **kwargs)

    def __str__(self):
        return self.event_name
    
@receiver(pre_delete, sender=Event)
def delete_event_images(sender, instance, **kwargs):
    # Delete associated images when an Event is deleted
    for folder in Folder.objects.filter(event=instance):
        for photo in Photo.objects.filter(folder=folder):
            image_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))
            if os.path.exists(image_path):
                os.remove(image_path)
            photo.delete()
        folder.delete()



class Folder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length = 255)
    created_by = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add=True)

    folder_credentials = models.CharField(max_length=255, default=uuid.uuid4, unique=True)

    def save(self, *args, **kwargs):
        if not self.folder_credentials:
            self.folder_credentials = str(uuid.uuid4())
        super(Folder, self).save(*args, **kwargs)

class Photo(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_filename)


    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    guest_name = models.CharField(max_length = 255, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)