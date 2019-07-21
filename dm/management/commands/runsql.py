from __future__ import absolute_import
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db import connection
from tabulate import tabulate


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('query')

    def handle(self, *args, **options):
        query = options[b'query']
        print query
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            headers = [i[0] for i in cursor.description]
            data = cursor.fetchall()
            print tabulate(data, headers=headers)
        except Exception as e:
            print 'Error occured:', e
        print
