import subprocess

import psutil as psutil
from django.core.management.commands.runserver import \
    Command as RunserverCommand


class Command(RunserverCommand):
    help = "AI model is called asynchronously so not blocking " \
           "the operation of the main application"

    def stop_existing_celery_worker(self):
        for process in psutil.process_iter(['pid', 'name']):
            if 'celery' in process.info['name']:
                process.terminate()
                self.stdout.write(
                    self.style.SUCCESS(
                        'terminate existing celery worker'))

    def handle(self, *args, **options):
        self.stop_existing_celery_worker()
        try:
            # Launch Celery worker alongside runserver
            celery_command = ['celery', '-A', 'recom_system', 'worker',
                              '--loglevel=INFO', '--hostname=rs_worker1']
            subprocess.Popen(celery_command)
            self.stdout.write(
                self.style.SUCCESS('Successfully starting celery worker'))
            # Call the original runserver command
            super().handle(*args, **options)
        except Exception as e:
            print(e)
            self.stop_existing_celery_worker()
