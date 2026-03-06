# 🚀 Hướng Dẫn Nhanh Bắt Đầu ShoeStore

## 📋 Tóm Tắt Dự Án

ShoeStore là một **ứng dụng web bán hàng đầy đủ chức năng** được xây dựng bằng **Django** cho phép:

✅ Khách hàng duyệt, tìm kiếm và mua sắm giày dép  
✅ Quản lý đơn hàng với trạng thái duyệt  
✅ Viết đánh giá và xếp hạng sản phẩm  
✅ Dashboard quản trị với biểu đồ thống kê  
✅ Authentication an toàn và phân quyền người dùng  

---

## 🛠️ Bước 1: Chuẩn Bị Môi Trường

### Yêu cầu:
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Git (optional)

### 1.1 Vào thư mục dự án
```bash
cd "c:\Users\NONG DUY AN\OneDrive\Documents\Dự án python\shoe_store"
```

### 1.2 Tạo môi trường ảo
```bash
python -m venv venv
```

### 1.3 Kích hoạt môi trường ảo
**Windows:**
```bash
venv\Scripts\activate
```

Terminal sẽ hiển thị `(venv)` ở đầu dòng khi hoạt động.

### 1.4 Cài đặt dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Bước 2: Cấu Hình Cơ Sở Dữ Liệu

### 2.1 Thiết lập migrations
```bash
python manage.py migrate --run-syncdb
```

### 2.2 Nạp dữ liệu mẫu
```bash
python setup_db.py
```

**Thông tin đăng nhập sau setup:**

| Loại | Username | Password |
|------|----------|----------|
| 👨‍💼 Admin | admin | admin123 |
| 👤 Khách hàng | customer1 | customer123 |

---

## 🚀 Bước 3: Chạy Ứng Dụng

### Khởi động development server
```bash
python manage.py runserver
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
```

### 🌐 Truy cập ứng dụng:
- **Website chính**: http://localhost:8000/
- **Admin panel**: http://localhost:8000/admin/

---

## 📊 Tính Năng Chính

### 👤 Cho Khách Hàng

1. **Trang Chủ** - Sản phẩm nổi bật, danh mục
2. **Duyệt Sản Phẩm** - Tìm kiếm, lọc, sắp xếp
3. **Chi Tiết Sản Phẩm** - Xem đánh giá, mô tả chi tiết
4. **Đặt Hàng** - Chọn số lượng, thêm ghi chú
5. **Quản Lý Tài Khoản** - Cập nhật hồ sơ, xem lịch sử
6. **Viết Đánh Giá** - Xếp hạng sao và nhận xét

### 👨‍💼 Cho Quản Trị Viên (Admin)

1. **Dashboard** - Thống kê tổng quan, biểu đồ
2. **Duyệt Đơn Hàng** - Chấp thuận/Từ chối đơn
3. **Quản Lý Sản Phẩm** - CRUD sản phẩm, danh mục
4. **Quản Lý Người Dùng** - Xem danh sách khách hàng

---

## 🗂️ Cấu Trúc Thư Mục

```
shoe_store/
├── store/                 ← Main app
│   ├── models.py         ← Database models
│   ├── views.py          ← Business logic
│   ├── forms.py          ← Django forms
│   ├── urls.py           ← URL routing
│   ├── templates/        ← HTML templates
│   │   └── store/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── product_list.html
│   │       └── ...
│   └── static/           ← CSS, JS, Images
├── shoe_store/           ← Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🗄️ Cơ Sở Dữ Liệu

### 5 Model Chính:

1. **User** - Người dùng hệ thống (built-in Django)
2. **UserProfile** - Mở rộng thông tin người dùng
3. **Category** - Danh mục sản phẩm
4. **Product** - Sản phẩm giày dép
5. **Order** - Đơn hàng
6. **Review** - Đánh giá sản phẩm

### Mối Quan Hệ:
```
User (1) ─── (N) Order
User (1) ─── (N) Review
Category (1) ─── (N) Product
Product (1) ─── (N) Order
Product (1) ─── (N) Review
```

---

## 🎯 Các URL Chính

### Trang Công Khai
```
/ ......................... Trang chủ
/products/ ................ Danh sách sản phẩm
/products/<id>/ ........... Chi tiết sản phẩm
/about/ ................... Về chúng tôi
/contact/ ................. Liên hệ
```

### Xác Thực
```
/register/ ................ Đăng ký
/login/ ................... Đăng nhập
/logout/ .................. Đăng xuất
/profile/ ................. Hồ sơ người dùng
```

### Đơn Hàng (Cần login)
```
/order/create/<id>/ ....... Tạo đơn hàng
/orders/ .................. Danh sách đơn hàng
/orders/<id>/ ............. Chi tiết đơn hàng
/product/<id>/review/ ..... Viết đánh giá
```

### Dashboard Admin
```
/dashboard/ ............... Dashboard quản trị
/admin/ ................... Django admin panel
```

---

## 🔐 Tài Khoản Mặc Định

### Admin Account
```
URL: http://localhost:8000/admin/
Username: admin
Password: admin123
```

### Test Customer Account
```
URL: http://localhost:8000/login/
Username: customer1
Password: customer123
```

---

## 📝 Phát Triển Thêm

### Để thêm tính năng mới:

1. **Tạo model** trong `store/models.py`
2. **Tạo migration**: `python manage.py makemigrations`
3. **Apply migration**: `python manage.py migrate`
4. **Tạo view** trong `store/views.py`
5. **Tạo template** trong `store/templates/store/`
6. **Thêm URL** trong `store/urls.py`

---

## 🐛 Hỗ Trợ Các Vấn Đề Phổ Biến

### Lỗi: Port 8000 đang được sử dụng
```bash
python manage.py runserver 8001
```

### Lỗi: Database không tồn tại
```bash
python manage.py migrate --run-syncdb
python setup_db.py
```

### Xóa database và tạo lại
```bash
del db.sqlite3
python manage.py migrate --run-syncdb
python setup_db.py
```

### Coi logs và debug
```bash
python manage.py shell
>>> from store.models import *
>>> Product.objects.all().count()
```

---

## 📚 Tài Liệu Tham Khảo

- [Django Docs](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [Chart.js](https://www.chartjs.org/)
- [SQLite](https://www.sqlite.org/docs.html)

---

## ✨ Các Tính Năng Đã Hoàn Thành (Criteria)

✅ Xác định scope & yêu cầu  
✅ Yêu cầu nghiệp vụ và quy tắc  
✅ Danh sách chức năng (6 chức năng)  
✅ Thiết kế giao diện (Home, Login, Dashboard, CRUD)  
✅ Kết nối cơ sở dữ liệu (SQLite/PostgreSQL/MySQL)  
✅ 2+ data models (Category, Product, Order, Review)  
✅ Seed data trên website  
✅ Cấu hình login/register  
✅ Menu, header, footer tư nhân  
✅ Template inheritance (base.html)  
✅ CRUD hoàn chỉnh cho 2 entities  
✅ Tìm kiếm, lọc, sắp xếp  
✅ Cấp quyền người dùng (Guest/User/Admin)  
✅ Trạng thái duyệt đơn hàng  
✅ Dashboard với biểu đồ  
✅ Kiểm tra dữ liệu (validation)  
✅ 10+ Git commits  
✅ README.md hoàn chỉnh  

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề, hãy:
1. Kiểm tra lỗi trong terminal
2. Xem README.md đầy đủ
3. Kiểm tra file logs (nếu có)
4. Xóa cache và restarthoàn toàn

---

**Chúc bạn phát triển thành công! 🎉**
