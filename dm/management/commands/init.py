from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from dm.models import MyModel


class Command(BaseCommand):
    def handle(self, *args, **options):

        if not User.objects.filter(username='admin').exists():
            print 'Creating superuser "admin": OK'
            user=User.objects.create_user('admin', password='adminadmin')
            user.is_superuser=True
            user.is_staff=True
            user.save()

        # if not MyModel.objects.all().exists():
        #     o = MyModel.objects.create()
        #     print 'Creating initial Model instance: OK {}'.format(vars(o))
