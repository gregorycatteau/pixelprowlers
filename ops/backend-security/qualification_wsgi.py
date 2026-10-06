"""Dedicated-fixture WSGI only, never a production settings module."""
from pathlib import Path
exec(Path(__file__).with_name('qualification.py').read_text().split('args=sys.argv[1:]')[0])
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
