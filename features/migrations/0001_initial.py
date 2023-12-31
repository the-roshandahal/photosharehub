# Generated by Django 5.0 on 2023-12-21 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('facebook_url', models.CharField(blank=True, max_length=200, null=True)),
                ('instagram_url', models.CharField(blank=True, max_length=200, null=True)),
                ('youtube_url', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
