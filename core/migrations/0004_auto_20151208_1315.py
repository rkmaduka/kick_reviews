# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.AddField(
            model_name='vote',
            name='comments',
            field=models.ForeignKey(blank=True, to='core.Comments', null=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='review',
            field=models.ForeignKey(blank=True, to='core.Review', null=True),
        ),
    ]
