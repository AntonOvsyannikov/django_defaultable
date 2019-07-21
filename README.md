# Django Defaultable Model 
*Django model with default instance, to which we can have ForeignKey with default value created automatically when needed*   

### Usage
```
# migrations/__init__.py

from dm.defaultable.stuff import monkey_patch_fields_operations
monkey_patch_fields_operations()
```
```
# models.py

from defaultable.models import Defaultable 

class ModelX(Defaultable): pass

class MyModel:
  x = ModelX.ForeignKey()
```
```
manage.py makemigrations
manage.py migrate
# voila!
```

You can test this works with different databases, using docker.

```
docker-compose -f docker-compose.yml -f docker-compose-mysql.yml up --build
```

or the same in scripts

```
test-mysql.sh
test-postgres.sh
test-sqlight.sh
```

or for host machine just run

```
entrypoint.sh
```

to test on sqlite.

### Explanation

It's often necessary to support relation between two models, where one of them has default
instance and other has ForeignKey with default value, associated with this default instance.

```
class ModelX: ...
class MyModel:
  x = models.ForeignKey (ModelX, default = ModelX.default_instance)
```

Also we want to keep data integrity, so ForeignKey should not be nullable and ModelX should always contain
at least one default object. 
 
Creation of such relation is quite tricky and includes multistage migrations making
with temporary violation of data integrity by creation of nullable ForeignKey and 
manual editing of Django migrations, like described in accepted answer on my question on StackOverflow:


[How to organize migration for two related models and automatically set default field value for id of newly created object?](https://stackoverflow.com/questions/56397090/how-to-organize-migration-for-two-related-models-and-automatically-set-default-f)


It's really inconvenient and can lead to some bad bugs i.e. during migration squashing.

This project provide solution with zero-efforts in migrations support, means we can still use automatic 
migrations making, squashing and even cleaning up the migration chain without any attention on creation 
of default instances. 

The idea is to provide callable for default of ForeignKey, which creates default instance of
referenced model, if it is not exists. But the problem is, that this callable can be called not 
only in final Django project stage, but also during migrations, with old project stages, so
it can be called for deleted model on early stages, when the model was still existing. 

The standard solution in RunPython operations is to use apps registry from the migration state,
but this feature unavailable for our callable, cause this registry is provided as
argument for RunPython and not available globally. But to support all scenarios of migration 
applying and rollback we need to detect are we in migration or not, and access appropriate apps registry.

The only solution is to monkey patch AddField and RemoveField operations to keep migration apps 
registry in global variable, if we are in migration.

```
migration_apps = None


def set_migration_apps(apps):
    global migration_apps
    migration_apps = apps


def get_or_create_default(model_name, app_name):
    M = (migration_apps or django.apps.apps).get_model(app_name, model_name)

    try:
        return M.objects.get(isDefault=True).id

    except M.DoesNotExist as e:
        o = M.objects.create(isDefault=True)
        print '{}.{} default object not found, creating default object : OK'.format(model_name, app_name)
        return o


def monkey_patch_fields_operations():
    def patch(klass):

        old_database_forwards = klass.database_forwards
        def database_forwards(self, app_label, schema_editor, from_state, to_state):
            set_migration_apps(to_state.apps)
            old_database_forwards(self, app_label, schema_editor, from_state, to_state)
        klass.database_forwards = database_forwards

        old_database_backwards = klass.database_backwards
        def database_backwards(self, app_label, schema_editor, from_state, to_state):
            set_migration_apps(to_state.apps)
            old_database_backwards(self, app_label, schema_editor, from_state, to_state)
        klass.database_backwards = database_backwards

    patch(django.db.migrations.AddField)
    patch(django.db.migrations.RemoveField)

```
