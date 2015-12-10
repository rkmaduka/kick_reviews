# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151210_1830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='visiblity',
            new_name='visibility',
        ),
    ]
