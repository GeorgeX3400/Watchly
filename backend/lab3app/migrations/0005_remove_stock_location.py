# Generated by Django 5.1.1 on 2025-01-15 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab3app', '0004_watch_updatedat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='location',
        ),
    ]
