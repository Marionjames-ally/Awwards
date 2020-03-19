# Generated by Django 3.0.4 on 2020-03-16 10:05

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('name', models.CharField(max_length=250)),
                ('caption', models.CharField(max_length=250)),
                ('link', models.URLField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(default='user', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='awards.Profile')),
            ],
        ),
    ]
