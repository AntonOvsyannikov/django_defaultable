import django.apps
import django.db.migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import ProjectState
from typing import Union

migration_apps = None


def set_migration_apps(apps):
    global migration_apps
    migration_apps = apps


def get_or_create_default(model_name, app_name):
    """ Returns default object of given model, creating it if not exist yet. """

    # This is the key to normal operation during migrations
    M = (migration_apps or django.apps.apps).get_model(app_name, model_name)

    try:
        return M.objects.get(isDefault=True).id

    except M.DoesNotExist as e:
        o = M.objects.create(isDefault=True)
        print '{}.{} default object not found, creating default object : OK'.format(model_name, app_name)
        return o


def monkey_patch_fields_operations():
    """ Monkey patch Django default fields operations.

    While getting default object we must know are we in migration or in normal
    Django environment to access correct app registry for model.
    It's not possible by default, so we do dirty hack - if we are in migrations, we
    store migration state in global variable during database_forwards and database_backwards
    operaions of AddField and RemoveField.

    To simplify migrations generation we'll monkey patch default AddField and RemoveField
    implementations, so we don't need to edit auto generated migrations.

    Call it in app.migrations.__init__. We can call it here and it works fine with AddField and
    forward migrations, but Django will not import this module to migration with RemoveField
    operation.
    """

    def patch(klass):
        """ Patch given Operation class. """

        old_database_forwards = klass.database_forwards

        def database_forwards(self, app_label, schema_editor, from_state, to_state):
            # print "====== {} database_forwards ========".format(klass.__name__)
            set_migration_apps(to_state.apps)
            old_database_forwards(self, app_label, schema_editor, from_state, to_state)

        klass.database_forwards = database_forwards

        old_database_backwards = klass.database_backwards

        def database_backwards(self, app_label, schema_editor, from_state, to_state):
            # print "====== {} database_backwards ========".format(klass.__name__)
            set_migration_apps(to_state.apps)
            old_database_backwards(self, app_label, schema_editor, from_state, to_state)

        klass.database_backwards = database_backwards

    # print "==== monkey_patch_fields_operations ===="
    patch(django.db.migrations.AddField)
    patch(django.db.migrations.RemoveField)
