# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comments_date',
            field=models.DateTimeField(default=datetime.date(2014, 12, 2)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comments',
            name='comments_text',
            field=models.TextField(verbose_name=b'Comments text'),
            preserve_default=True,
        ),
    ]
