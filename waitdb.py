import os
from time import sleep

settings = os.environ.get('ENV_SETTINGS')

if settings == 'mysql':
    import MySQLdb

    while True:
        try:
            db = MySQLdb.connect(host = 'db', user = 'user', passwd = 'password', db = 'dmtest')
        except Exception:
            print "Database not ready, waiting..."
        else:
            break
        sleep(1)


elif settings=='postgres':

    import psycopg2

    while True:
        try:
            db = psycopg2.connect("dbname='dmtest' user='user' host='db' password='password' connect_timeout=1 ")
        except Exception:
            print "Database not ready, waiting..."
        else:
            break
        sleep(1)

sleep(0.5)
print "Database is ready!"

