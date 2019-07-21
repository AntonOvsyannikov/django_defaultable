# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from dm.defaultable.stuff import set_migration_apps


def create_mymodel_instance(apps, schema_editor):
    set_migration_apps(apps)
    M = apps.get_model('dm', 'MyModel')
    M.objects.create()


def do_nothing(apps, schema_editor): pass


class Migration(migrations.Migration):
    dependencies = [
        ('dm', '0002_auto_20190720_2009'),
    ]

    operations = [
        migrations.RunPython(create_mymodel_instance, reverse_code=do_nothing)
    ]
