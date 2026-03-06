#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from django.contrib.auth.models import User

superusers = User.objects.filter(is_superuser=True)
print(f"Superuser count: {superusers.count()}")

if superusers.count() > 0:
    for user in superusers:
        print(f"  - {user.username}")
else:
    print("No superuser found. Creating admin account...")
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print("Admin account created: username=admin, password=admin123")
