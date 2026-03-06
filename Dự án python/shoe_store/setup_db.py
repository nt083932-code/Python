import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, UserProfile

# Create superuser
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    admin_profile = UserProfile.objects.get(user=admin)
    admin_profile.user_type = 'admin'
    admin_profile.save()
    print("✓ Admin user created successfully!")
else:
    print("✓ Admin user already exists!")

# Create test customer
if not User.objects.filter(username='customer1').exists():
    customer = User.objects.create_user(
        username='customer1',
        email='customer@example.com',
        password='customer123',
        first_name='Nguyễn',
        last_name='Văn A'
    )
    customer_profile = UserProfile.objects.get(user=customer)
    customer_profile.phone = '0123456789'
    customer_profile.address = '123 Đường ABC'
    customer_profile.city = 'Hà Nội'
    customer_profile.user_type = 'customer'
    customer_profile.save()
    print("✓ Test customer created successfully!")
else:
    print("✓ Test customer already exists!")

# Create categories
categories_data = [
    {'name': 'Giày Sneaker', 'description': 'Giày thể thao thoải mái'},
    {'name': 'Dép Xỏ Ngón', 'description': 'Dép nhẹ và thoáng'},
    {'name': 'Giày Boot', 'description': 'Giày ống cao ấm áp'},
    {'name': 'Giày Lịch Sự', 'description': 'Giày công sở chuyên nghiệp'},
]

for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description'], 'is_active': True}
    )
    if created:
        print(f"✓ Created category: {cat.name}")

# Create products
print("\nCreating sample products...")
categories = {cat.name: cat for cat in Category.objects.all()}

products_data = [
    {
        'name': 'Nike Air Force 1',
        'description': 'Giày sneaker huyền thoại của Nike với thiết kế classic',
        'price': 1200000,
        'category': 'Giày Sneaker',
        'shoe_type': 'sneaker',
        'size': '42',
        'color': 'Trắng',
        'material': 'Da lộn',
        'brand': 'Nike',
        'quantity_in_stock': 15,
        'is_featured': True,
    },
    {
        'name': 'Adidas Ultra Boost',
        'description': 'Giày chạy bộ hiệu năng cao với công nghệ Boost',
        'price': 1500000,
        'category': 'Giày Sneaker',
        'shoe_type': 'sneaker',
        'size': '40',
        'color': 'Đen',
        'material': 'Vải',
        'brand': 'Adidas',
        'quantity_in_stock': 10,
        'is_featured': True,
    },
    {
        'name': 'Dép Havaianas',
        'description': 'Dép xỏ ngón thoải mái cho mua hè',
        'price': 300000,
        'category': 'Dép Xỏ Ngón',
        'shoe_type': 'sandal',
        'size': '38',
        'color': 'Xanh',
        'material': 'Cao su',
        'brand': 'Havaianas',
        'quantity_in_stock': 50,
        'is_featured': False,
    },
    {
        'name': 'Timberland Boot',
        'description': 'Giày boot bền bỉ cho các chuyến phiêu lưu',
        'price': 2500000,
        'category': 'Giày Boot',
        'shoe_type': 'boot',
        'size': '43',
        'color': 'Nâu',
        'material': 'Da thật',
        'brand': 'Timberland',
        'quantity_in_stock': 8,
        'is_featured': False,
    },
    {
        'name': 'Oxford Formal',
        'description': 'Giày lịch sự chuyên dụng cho công sở',
        'price': 1800000,
        'category': 'Giày Lịch Sự',
        'shoe_type': 'formal',
        'size': '41',
        'color': 'Đen',
        'material': 'Da bò',
        'brand': 'Clarks',
        'quantity_in_stock': 12,
        'is_featured': True,
    },
]

for prod_data in products_data:
    category = categories[prod_data.pop('category')]
    defaults = prod_data.copy()
    defaults['category'] = category
    
    prod, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults=defaults
    )
    if created:
        print(f"✓ Created product: {prod.name}")

print("\n✅ Database seeding completed successfully!")
print("\nAdmin credentials:")
print("  Username: admin")
print("  Password: admin123")
print("\nTest customer credentials:")
print("  Username: customer1")
print("  Password: customer123")
