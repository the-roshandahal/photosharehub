# Generated by Django 5.0 on 2023-12-20 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='locaton',
            new_name='location',
        ),
    ]
