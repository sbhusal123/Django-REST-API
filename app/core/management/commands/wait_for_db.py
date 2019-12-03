import time
from django.db import connections
from django.db import OperationalError
from django.core.management.base import BaseCommand

"""
Custom Management Command: https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/#module-django.core.management
connections => Returns an object to handle connection. Have a look at original code from at site package.
""" # noqa


class Command(BaseCommand):
    """Django command to pause execution until database is available."""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database ...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting for 1 second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
