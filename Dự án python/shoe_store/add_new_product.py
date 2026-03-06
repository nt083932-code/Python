import os
import django
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from store.models import Product, Category

def create_sample_image(product_name, filename):
    """Create a sample image for the product"""
    # Create a 400x400 image
    img = Image.new('RGB', (400, 400), color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
    draw = ImageDraw.Draw(img)

    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    # Add text
    text = f"{product_name}\nShoe Store"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (400 - text_width) // 2
    y = (400 - text_height) // 2

    draw.text((x, y), text, fill='white', font=font)

    # Save the image
    img.save(filename)

def add_new_product():
    """Add a new sample product with image"""
    # Get a random category
    categories = list(Category.objects.all())
    if not categories:
        print("No categories found!")
        return

    category = random.choice(categories)

    # Create product data
    product_name = f"New Shoe {random.randint(100, 999)}"
    product_data = {
        'name': product_name,
        'brand': 'Sample Brand',
        'description': f'A beautiful {category.name.lower()} from our collection.',
        'price': random.randint(50, 200),
        'quantity_in_stock': random.randint(10, 50),
        'category': category,
        'is_active': True,
    }

    # Create the product
    product = Product.objects.create(**product_data)
    print(f"Created product: {product.name}")

    # Create and attach image
    image_filename = f"media/products/{product_name.replace(' ', '_').lower()}.jpg"
    create_sample_image(product_name, image_filename)

    # Attach image to product
    with open(image_filename, 'rb') as f:
        product.image.save(f"{product_name.replace(' ', '_').lower()}.jpg", File(f), save=True)

    print(f"Added image to product: {product.image.url}")
    print(f"Product added successfully: {product.name} in {category.name}")
if __name__ == '__main__':
    add_new_product()
