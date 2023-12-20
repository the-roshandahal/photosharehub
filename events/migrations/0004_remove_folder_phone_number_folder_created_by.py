# Generated by Django 5.0 on 2023-12-20 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_folder_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='folder',
            name='created_by',
            field=models.CharField(default='dsa', max_length=200),
            preserve_default=False,
        ),
    ]