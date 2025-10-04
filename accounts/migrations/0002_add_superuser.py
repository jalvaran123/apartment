from django.db import migrations

def add_superuser(apps, schema_editor):
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, date_joined, first_name, last_name, email)
                VALUES ('cookie', 'pbkdf2_sha256$1000000$m0y8ULZBtlM1DNYP6e6aam$PTEWfxeNgshTDYRYgBzXiiIH7vd+1rIRvVVXW9JiCBA=', TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, '', '', 'Virjunlargo6@Gmail.com')
                ON CONFLICT (username) DO NOTHING
            """)
            print("Superuser migration executed successfully")
    except Exception as e:
        print(f"Error in superuser migration: {e}")

def reverse_add_superuser(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM auth_user WHERE username = 'cookie'")

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),  # Correct dependency
    ]
    operations = [
        migrations.RunPython(add_superuser, reverse_code=reverse_add_superuser),
    ]