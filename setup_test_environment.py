import os
import sys

import django


def setup_django_environment():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'recom_system.settings'

    django_project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'recom_system'))
    sys.path.append(django_project_dir)

    django.setup()


if __name__ == '__main__':
    setup_django_environment()
