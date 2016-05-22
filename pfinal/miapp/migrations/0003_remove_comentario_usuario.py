# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0002_hotel_ncomentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='usuario',
        ),
    ]
