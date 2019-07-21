#!/bin/bash

if [ "$ENV_SETTINGS" ]; then python waitdb.py; fi

echo "
=========================================================================================

There are following Models in the project:

class ModelX(Defaultable): pass
class ModelY(Defaultable): pass

class MyModel(models.Model):
    x = ModelX.ForeignKey()
    y = ModelY.ForeignKey()

They are created and initialized, and then removed, using following migrations sequence:

0001: Create MyModel
0002: Create ModelX and x field in MyModel
0003: Create MyModel instance
0004: Remove ModelX and x field in MyModel
0005: Create ModelY and y field in MyModel

So let's test how it works.
"
echo "
=========================
manage migrate dm 0001: Create MyModel, no ModelX yet so we got the error in SELECT
"
python manage.py migrate dm 0001
python manage.py runsql 'SELECT * FROM dm_modelx'
python manage.py runsql 'SELECT * FROM dm_mymodel'
echo "
=========================
manage migrate dm 0001: Create ModelX and x field in MyModel. Even there is not MyModel 
instance yet the default ModelX instance created, cause get_or_create_default called 
during x field creation. Take a note ! There is no ModelX already in the project, but Django 
still can create default ModelX instance using ProjectState from the past!
"
python manage.py migrate dm 0002
python manage.py runsql 'SELECT * FROM dm_modelx'
python manage.py runsql 'SELECT * FROM dm_mymodel'
echo "
=========================
manage migrate dm 0003: Create MyModel instance with x field pointed to default ModelX object
Take a note, if you need to use RunPython in migrations you should 
"
python manage.py migrate dm 0003
python manage.py runsql 'SELECT * FROM dm_modelx'
python manage.py runsql 'SELECT * FROM dm_mymodel'
echo "
=========================
manage migrate dm 0004: Remove ModelX and x field in MyModel, no ModelX so error in SELECT
"
python manage.py migrate dm 0004
python manage.py runsql 'SELECT * FROM dm_modelx'
python manage.py runsql 'SELECT * FROM dm_mymodel'
echo "
=========================
manage migrate dm 0003: Rollback last migration, so Django rollbacks RemoveField operation, 
means re-create x field in the model At this moment default ModelX instance will be re-created 
in get_or_create_default operation. Take a note, that monkey patching of AddField and RemoveField 
is necessary to prepare global environment for get_or_create_default, otherwise it can not get 
corect apps registry of current project state.
"
python manage.py migrate dm 0003
python manage.py runsql 'SELECT * FROM dm_modelx'
python manage.py runsql 'SELECT * FROM dm_mymodel'
echo "
=========================
manage migrate: Migrate project to final state
manage init: Creates superuser admin:adminadmin

You can do manage.py runserver 0.0.0.0:8000 now and check how it works in django admin.
Take a note how data integrity of Defaultable objects is supported. Feel free to create
and remove defaultable objects and fields, make migrations, and apply or rollback it.
No additional efforts to support it in automatically generated migrations.
"
python manage.py migrate
python manage.py init
python manage.py runsql 'SELECT * FROM dm_modelx'
python manage.py runsql 'SELECT * FROM dm_modely'
python manage.py runsql 'SELECT * FROM dm_mymodel'

python manage.py runserver 0.0.0.0:8000


