import os
import sys

# Ensure project root directory is in the Python search path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')

import django
django.setup()

# On Vercel serverless environment, auto-apply migrations and seed if database is new
if os.getenv('VERCEL') == '1':
    try:
        from django.core.management import call_command
        from core.models import User
        # If user table does not exist or has no users, migrate and seed
        if not User.objects.exists():
            call_command('migrate', interactive=False)
            from core.seed_data import run_seed
            run_seed()
    except Exception:
        try:
            from django.core.management import call_command
            call_command('migrate', interactive=False)
            from core.seed_data import run_seed
            run_seed()
        except Exception:
            pass

from saferide_project.wsgi import application

app = application
