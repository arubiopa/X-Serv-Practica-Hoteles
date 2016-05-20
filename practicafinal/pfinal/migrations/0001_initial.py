# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160517050722 on 2016-05-19 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=32)),
                ('comentario', models.TextField(max_length=300)),
                ('hotelId', models.IntegerField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('body', models.TextField(max_length=600)),
                ('web', models.URLField()),
                ('cat', models.TextField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='HotelSeleccionado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotelId', models.IntegerField()),
                ('usuario', models.CharField(max_length=32)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotelId', models.IntegerField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='PagCSS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=32)),
                ('titulo', models.CharField(max_length=32)),
                ('colorFondo', models.TextField()),
            ],
        ),
    ]
