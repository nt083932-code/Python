import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from store.models import Product

products = Product.objects.all()
print('Products:')
for p in products:
    image_status = p.image.url if p.image else "No image"
    print(f'- {p.name} ({p.category.name}) - Image: {image_status}')
print(f'Total: {products.count()} products')