#!/usr/bin/env python3
"""
Database Diagnostic Script
Run this to diagnose database and migration issues
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
django.setup()

from django.db import connection, connections
from django.core.management import call_command
from django.conf import settings
import django.db.utils

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def print_warning(text):
    print(f"⚠ {text}")

def print_info(text):
    print(f"ℹ {text}")

print_header("DATABASE DIAGNOSTICS")

# 1. Check database settings
print_info("Checking database configuration...")
db_settings = settings.DATABASES['default']
print(f"  Engine: {db_settings['ENGINE']}")
print(f"  Name: {db_settings['NAME']}")
print(f"  User: {db_settings['USER']}")
print(f"  Host: {db_settings['HOST']}")
print(f"  Port: {db_settings['PORT']}")
print()

# 2. Test database connection
print_info("Testing database connection...")
try:
    connection.ensure_connection()
    print_success("Successfully connected to database!")
except Exception as e:
    print_error(f"Failed to connect to database: {e}")
    print()
    print("Troubleshooting steps:")
    print("  1. Make sure MySQL is running:")
    print("     sc query MySQL80")
    print("     net start MySQL80")
    print()
    print("  2. Check your .env file or environment variables:")
    print(f"     DB_HOST={db_settings['HOST']}")
    print(f"     DB_PORT={db_settings['PORT']}")
    print(f"     DB_USER={db_settings['USER']}")
    print(f"     DB_PASSWORD=<check your password>")
    print()
    print("  3. Create database if it doesn't exist:")
    print("     mysql -u root -p")
    print(f"     CREATE DATABASE {db_settings['NAME']};")
    sys.exit(1)

print()

# 3. Check if database exists
print_info("Checking if database exists...")
try:
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW DATABASES LIKE '{db_settings['NAME']}'")
        result = cursor.fetchone()
        if result:
            print_success(f"Database '{db_settings['NAME']}' exists")
        else:
            print_error(f"Database '{db_settings['NAME']}' does NOT exist")
            print()
            print("Create it with:")
            print(f"  mysql -u root -p")
            print(f"  CREATE DATABASE {db_settings['NAME']};")
            sys.exit(1)
except Exception as e:
    print_error(f"Error checking database: {e}")
    sys.exit(1)

print()

# 4. Check existing tables
print_info("Checking existing tables...")
try:
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            print_success(f"Found {len(tables)} table(s):")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Check for users table specifically
            table_names = [t[0] for t in tables]
            if 'users' in table_names:
                print()
                print_success("'users' table exists!")
                
                # Show structure
                cursor.execute("DESCRIBE users")
                columns = cursor.fetchall()
                print()
                print("Table structure:")
                for col in columns:
                    print(f"  {col[0]}: {col[1]}")
            else:
                print()
                print_warning("'users' table does NOT exist")
                print("Need to run migrations!")
        else:
            print_warning("No tables found in database")
            print("Need to run migrations!")
except Exception as e:
    print_error(f"Error checking tables: {e}")

print()

# 5. Check migrations
print_info("Checking migrations...")
try:
    from django.db.migrations.recorder import MigrationRecorder
    recorder = MigrationRecorder(connection)
    applied_migrations = recorder.applied_migrations()
    
    if applied_migrations:
        print_success(f"Found {len(applied_migrations)} applied migration(s):")
        users_migrations = [m for m in applied_migrations if m[0] == 'users']
        if users_migrations:
            for app, name in users_migrations:
                print(f"  - {app}: {name}")
        else:
            print_warning("No migrations applied for 'users' app")
    else:
        print_warning("No migrations have been applied yet")
except Exception as e:
    print_warning(f"Could not check migrations: {e}")

print()

# 6. Check migration files
print_info("Checking migration files...")
migrations_dir = os.path.join(os.path.dirname(__file__), 'users', 'migrations')
if os.path.exists(migrations_dir):
    migration_files = [f for f in os.listdir(migrations_dir) 
                      if f.endswith('.py') and f != '__init__.py']
    if migration_files:
        print_success(f"Found {len(migration_files)} migration file(s):")
        for f in sorted(migration_files):
            print(f"  - {f}")
    else:
        print_warning("No migration files found!")
        print("Need to create migrations!")
else:
    print_error("Migrations directory doesn't exist!")

print()

# 7. Recommendations
print_header("RECOMMENDATIONS")

try:
    # Check if users table exists
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE 'users'")
        users_table_exists = cursor.fetchone() is not None
    
    if not users_table_exists:
        print("The 'users' table doesn't exist. Follow these steps:")
        print()
        print("Step 1: Create migrations")
        print("  python manage.py makemigrations users")
        print()
        print("Step 2: Apply migrations")
        print("  python manage.py migrate")
        print()
        print("Step 3: If that doesn't work, force sync:")
        print("  python manage.py migrate --run-syncdb")
        print()
        print("Step 4: Verify table was created:")
        print("  python manage.py dbshell")
        print("  SHOW TABLES;")
        print("  DESCRIBE users;")
    else:
        print_success("Everything looks good! The 'users' table exists.")
        print()
        print("You can now:")
        print("  1. Start the server:")
        print("     python manage.py runserver")
        print()
        print("  2. Access the API:")
        print("     http://localhost:8000/api/users/")
        print()
        print("  3. Create a test user:")
        print("     python test_api.py")

except Exception as e:
    print_error(f"Error during final check: {e}")

print()
print("=" * 70)

