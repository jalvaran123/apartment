import django
import os
import sys
from django.db import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment.settings')
try:
    django.setup()
except Exception as e:
    print(f"Failed to setup Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User

try:
    username = 'cookie'
    email = 'Virjunlargo6@Gmail.com'
    password_hash = 'pbkdf2_sha256$1000000$m0y8ULZBtlM1DNYP6e6aam$PTEWfxeNgshTDYRYgBzXiiIH7vd+1rIRvVVXW9JiCBA='

    if not User.objects.filter(username=username).exists():
        user = User.objects.create(
            username=username,
            email=email,
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.password = password_hash
        user.save()
        print("Superuser created successfully")
    else:
        print("Superuser already exists")
except OperationalError as e:
    print(f"Database error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)