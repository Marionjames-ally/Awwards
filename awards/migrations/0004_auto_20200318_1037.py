# Generated by Django 3.0.4 on 2020-03-18 07:37

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0003_auto_20200318_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=cloudinary.models.CloudinaryField(default='image', max_length=255, verbose_name='image'),
        ),
    ]