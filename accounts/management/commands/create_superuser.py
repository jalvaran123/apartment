from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser non-interactively'

    def handle(self, *args, **options):
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
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))