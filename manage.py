#!/usr/local/bin/python3.7
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailFresh.settings')

    from django.core.management import execute_from_command_line

    # !/usr/bin/env python

    # try:
    #     from django.core.management import execute_from_command_line
    # except ImportError as exc:
    #     raise ImportError(
    #         "Couldn't import Django. Are you sure it's installed and "
    #         "available on your PYTHONPATH environment variable? Did you "
    #         "forget to activate a virtual environment?"
    #     # ) from exc
    #     )exc
    execute_from_command_line(sys.argv)
