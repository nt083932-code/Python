"""
Script to add sample images to existing products and create new products with images
"""

import os
import django
from django.core.files.base import ContentFile
from PIL import Image
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoe_store.settings')
django.setup()

from store.models import Product, Category

def create_sample_image(color_code, text):
    """Create a sample shoe image with PIL"""
    img = Image.new('RGB', (300, 300), color=color_code)
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return img_io

def add_images_to_existing_products():
    """Add sample images to existing products without images"""
    products = Product.objects.filter(image='')
    count = 0
    
    for product in products:
        try:
            # Assign colors based on shoe type
            colors = {
                'sneaker': (255, 200, 100),  # Orange-ish
                'boot': (100, 80, 60),  # Brown
                'sandal': (200, 180, 150),  # Tan
                'formal': (50, 50, 50),  # Dark gray
                'casual': (150, 150, 180),  # Blue-gray
            }
            color = colors.get(product.shoe_type, (200, 200, 200))
            
            img_io = create_sample_image(color, product.name)
            filename = f"{product.id}_sample.jpg"
            product.image.save(filename, ContentFile(img_io.getvalue()), save=True)
            print(f"✓ Added image to: {product.name}")
            count += 1
        except Exception as e:
            print(f"✗ Error adding image to {product.name}: {e}")
    
    print(f"\nTotal images added: {count}")

def list_all_products():
    """List all products in database"""
    products = Product.objects.all()
    print("\n" + "="*60)
    print("DANH SÁCH SẢN PHẨM HIỆN CÓ")
    print("="*60)
    for p in products:
        has_image = "✓ Có hình" if p.image else "✗ Không có hình"
        print(f"ID: {p.id:2d} | {p.name:30s} | {has_image}")
    print(f"\nTổng: {products.count()} sản phẩm")

def show_instructions():
    """Show instructions for adding new products"""
    print("\n" + "="*60)
    print("HƯỚNG DẪN THÊM SẢN PHẨM MỚI")
    print("="*60)
    print("""
1. VÀO ADMIN PANEL:
   - URL: http://127.0.0.1:8000/admin/
   - Đăng nhập tài khoản admin

2. THÊM SẢN PHẨM MỚI:
   - Click: STORE > Products
   - Click: "ADD PRODUCT" (góc phải)

3. ĐIỀN THÔNG TIN:
   - Name: Tên giày (bắt buộc)
   - Description: Mô tả sản phẩm
   - Category: Chọn danh mục*
   - Shoe type: Loại giày*
   - Size: Kích cỡ (ví dụ: 42)*
   - Color: Màu sắc*
   - Material: Chất liệu*
   - Brand: Thương hiệu*
   - Price: Giá bán (ví dụ: 2500000)*
   - Quantity in stock: Số lượng*
   - Image: Upload hình ảnh**
   - Is Featured: Check để nổi bật
   - Is Active: Check để hiển thị

   * Bắt buộc điền
   ** Upload hình ảnh (JPG, PNG, GIF < 2MB)

4. LƯU SẢN PHẨM:
   - Click "SAVE" để lưu
   - Click "Save and add another" để thêm sản phẩm tiếp theo

📝 DANH MỤC HIỆN CÓ:
    """)
    cats = Category.objects.all()
    for cat in cats:
        print(f"   • {cat.name}")
    
    print(f"""
✅ LOẠI GIÀY:
   • sneaker (Giày thể thao)
   • boot (Giày ủng)
   • sandal (Dép)
   • formal (Giày lịch sự)
   • casual (Giày thường ngày)

💾 HÌNH ẢNH:
   • Định dạng: JPG, PNG, GIF
   • Kích thước: Tối đa 2MB
   • Tên file: Không dấu cách
   • Ví dụ: nike_air_max.jpg

🎯 TIPS:
   • Sản phẩm sẽ hiển thị ngay trên website
   • Check "Is Featured" để nổi bật trên trang chủ
   • Có thể sửa lại sau bằng cách click tên sản phẩm
""")

if __name__ == '__main__':
    print("\n🚀 SCRIPT THÊM HÌNH ẢNH VÀ SẢN PHẨM")
    print("="*60)
    
    # Add images to existing products
    print("\n📸 THÊM HÌNH ẢNH CHO SẢN PHẨM HIỆN CÓ...")
    add_images_to_existing_products()
    
    # List all products
    list_all_products()
    
    # Show instructions
    show_instructions()
    
    print("\n✅ Script hoàn tất!")
