import os
import django
from django.core.wsgi import get_wsgi_application

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment.settings')

# Setup Django
django.setup()

# Run migrations at startup
from django.core.management import call_command
from django.contrib.auth import get_user_model

try:
    call_command('migrate', interactive=False)
    print("Startup: migrations applied successfully")

    # Create superuser if it doesn't exist
    User = get_user_model()
    if not User.objects.filter(username="cookie").exists():
        User.objects.create_superuser("cookie", "Virjunlargo6@Gmail.com", "Cookie12345")
        print("Startup: created superuser 'cookie'")
    else:
        print("Startup: superuser 'cookie' already exists")

except Exception as e:
    print(f"Startup error: {e}")

# Standard WSGI application
application = get_wsgi_application()
