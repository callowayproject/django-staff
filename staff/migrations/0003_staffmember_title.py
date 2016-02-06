# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_remove_staffmember_sites'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='title',
            field=models.CharField(default=b'', max_length=50, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
