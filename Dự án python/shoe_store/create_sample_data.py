from store.models import Category, Product
from django.core.files.base import ContentFile
from PIL import Image
import io

def create_sample_data():
    # Create categories
    categories = ['Sneakers', 'Sandals', 'Boots', 'Formal Shoes']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name, defaults={'description': f'{cat_name} category'})

    # Get categories
    sneakers_cat = Category.objects.get(name='Sneakers')
    sandals_cat = Category.objects.get(name='Sandals')

    # Sample products data
    products_data = [
        {
            'name': 'Nike Air Max 90',
            'description': 'Classic Nike sneakers with Air Max technology',
            'price': 2500000,
            'category': sneakers_cat,
            'shoe_type': 'sneaker',
            'size': '42',
            'color': 'White/Black',
            'material': 'Synthetic/Leather',
            'brand': 'Nike',
            'quantity_in_stock': 15,
            'is_featured': True
        },
        {
            'name': 'Adidas Ultraboost',
            'description': 'Comfortable running shoes with Boost technology',
            'price': 3200000,
            'category': sneakers_cat,
            'shoe_type': 'sneaker',
            'size': '41',
            'color': 'Black',
            'material': 'Primeknit',
            'brand': 'Adidas',
            'quantity_in_stock': 8
        },
        {
            'name': 'Birkenstock Arizona',
            'description': 'Comfortable sandals with adjustable straps',
            'price': 1800000,
            'category': sandals_cat,
            'shoe_type': 'sandal',
            'size': '40',
            'color': 'Brown',
            'material': 'Leather',
            'brand': 'Birkenstock',
            'quantity_in_stock': 12
        },
        {
            'name': 'Converse Chuck Taylor',
            'description': 'Iconic high-top sneakers',
            'price': 1500000,
            'category': sneakers_cat,
            'shoe_type': 'sneaker',
            'size': '43',
            'color': 'Navy Blue',
            'material': 'Canvas',
            'brand': 'Converse',
            'quantity_in_stock': 20,
            'is_featured': True
        }
    ]

    # Create products
    created_count = 0
    for data in products_data:
        try:
            product = Product.objects.create(**data)
            print(f'✓ Created product: {product.name} (ID: {product.id})')
            created_count += 1
        except Exception as e:
            print(f'✗ Error creating {data["name"]}: {e}')

    print(f'\nTotal products created: {created_count}')
    print(f'Total products in database: {Product.objects.count()}')

if __name__ == '__main__':
    create_sample_data()