from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, UserProfile
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting seed data...')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@shoestore.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            admin_profile = UserProfile.objects.get(user=admin)
            admin_profile.user_type = 'admin'
            admin_profile.save()
            self.stdout.write(self.style.SUCCESS('Admin user created'))

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
            self.stdout.write(self.style.SUCCESS('Test customer created'))

        # Create categories
        categories_data = [
            {'name': 'Giày Sneaker', 'description': 'Giày thể thao thoải mái'},
            {'name': 'Dép Xỏ Ngón', 'description': 'Dép nhẹ và thoáng'},
            {'name': 'Giày Boot', 'description': 'Giày ống cao ấm áp'},
            {'name': 'Giày Lịch Sự', 'description': 'Giày công sở chuyên nghiệp'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description'], 'is_active': True}
            )
            categories[cat.name] = cat
            if created:
                self.stdout.write(f'Created category: {cat.name}')

        # Create products
        products_data = [
            {
                'name': 'Nike Air Force 1',
                'description': 'Giày sneaker huyền thoại của Nike',
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
                'description': 'Giày chạy bộ hiệu năng cao',
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
                'description': 'Dép xỏ ngón thoải mái',
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
                'description': 'Giày boot bền bỉ',
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
                'description': 'Giày lịch sự cho công sở',
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
                self.stdout.write(f'Created product: {prod.name}')

        self.stdout.write(self.style.SUCCESS('Seed data completed successfully!'))
