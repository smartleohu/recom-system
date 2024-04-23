import os
import sys

import django


def setup_django_environment():
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recom_system.settings')

    # Add the project directory to the Python path
    django_project_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'recom_system'))
    sys.path.append(django_project_dir)

    # Initialize Django
    django.setup()


if __name__ == '__main__':
    try:
        # Set up the Django environment
        setup_django_environment()
        print("Django environment setup successful.")
    except Exception as e:
        # Print any errors that occur during setup
        print(f"Error setting up Django environment: {e}")
