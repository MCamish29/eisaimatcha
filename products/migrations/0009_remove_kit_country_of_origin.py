# Generated by Django 3.2.25 on 2025-04-08 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_kit_country_of_origin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kit',
            name='country_of_origin',
        ),
    ]
