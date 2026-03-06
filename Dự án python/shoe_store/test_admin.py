#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from store.admin import ProductAdmin
from store.models import Product
from django.contrib.auth.models import User
from django.contrib import admin

print("Testing ProductAdmin initialization...")
try:
    admin_user = User.objects.filter(is_superuser=True).first()
    product_admin = ProductAdmin(Product, admin.site)
    print("✓ ProductAdmin initialized successfully")
    print(f"  - list_display: {product_admin.list_display}")
    print(f"  - list_filter: {product_admin.list_filter}")
    print(f"  - search_fields: {product_admin.search_fields}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
