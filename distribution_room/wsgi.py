"""
WSGI config for distribution_room project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "distribution_room.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(...)
    execute_from_command_line(sys.argv)

