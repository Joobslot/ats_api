import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Comando que detiene la ejecución hasta que la base este lista"""

    def handle(self, *args, **options):
        self.stdout.write('🚦 Esperando a la base de datos...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('⏰ Esperando 1 segundo...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('🚀 Base de datos disponible!'))
