# ShoeStore - Website Bán Giày Dép

Một ứng dụng web đầy đủ chức năng xây dựng với Django để quản lý và bán giày dép trực tuyến. Dự án bao gồm các chức năng quan trọng như quản lý sản phẩm, đơn hàng, người dùng, và dashboard quản trị.

## 📋 Mục Lục

- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Cấu Hình](#cấu-hình)
- [Chạy Ứng Dụng](#chạy-ứng-dụng)
- [Tính Năng](#tính-năng)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [Cơ Sở Dữ Liệu](#cơ-sở-dữ-liệu)
- [API & URL](#api--url)

## 🔧 Yêu Cầu Hệ Thống

- Python 3.8 hoặc cao hơn
- pip (Python package manager)
- SQLite3 (đi kèm với Python)

## 📦 Cài Đặt

### 1. Clone hoặc tải dự án

```bash
cd "c:\Users\NONG DUY AN\OneDrive\Documents\Dự án python\shoe_store"
```

### 2. Tạo môi trường ảo (Virtual Environment)

```bash
python -m venv venv
```

### 3. Kích hoạt môi trường ảo

**Trên Windows:**
```bash
venv\Scripts\activate
```

**Trên Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

## ⚙️ Cấu Hình

### 1. Cấu hình file .env

Mở file `.env` và cập nhật các giá trị:

```env
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=db.sqlite3
```

### 2. Khởi tạo cơ sở dữ liệu

Chạy migrations:
```bash
python manage.py migrate
```

### 3. Tạo super user (Admin)

```bash
python manage.py createsuperuser
```

Nhập thông tin:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

### 4. Nạp dữ liệu mẫu (Seed Data)

```bash
python manage.py seed_data
```

Lệnh này sẽ tạo:
- Admin user (username: admin, password: admin123)
- Test customer (username: customer1, password: customer123)
- 4 danh mục sản phẩm
- 5 sản phẩm mẫu

## 🚀 Chạy Ứng Dụng

### Phát triển (Development)

```bash
python manage.py runserver
```

Truy cập ứng dụng tại: `http://localhost:8000/`

Truy cập admin panel: `http://localhost:8000/admin/`

### Công nhân tĩnh (Static Files)

Để thu thập static files:
```bash
python manage.py collectstatic
```

## ✨ Tính Năng

### 👤 Chức Năng Người Dùng Khách

1. **Duyệt Sản Phẩm**
   - Xem danh sách sản phẩm
   - Tìm kiếm theo tên, thương hiệu
   - Lọc theo danh mục, giá
   - Sắp xếp theo giá, đánh giá, ngày tạo

2. **Chi Tiết Sản Phẩm**
   - Xem thông tin chi tiết sản phẩm
   - Xem đánh giá từ khách hàng khác
   - Xem sản phẩm liên quan

3. **Đặt Hàng**
   - Chọn số lượng sản phẩm
   - Thêm ghi chú cho đơn hàng
   - Xem tổng tiền tự động

4. **Quản Lý Tài Khoản**
   - Đăng ký tài khoản mới
   - Đăng nhập/Đăng xuất
   - Cập nhật hồ sơ cá nhân
   - Xem lịch sử đơn hàng

5. **Đánh Giá Sản Phẩm**
   - Viết đánh giá cho sản phẩm đã mua
   - Chỉnh sửa đánh giá của mình
   - Xem đánh giá của người khác

### 👨‍💼 Chức Năng Quản Trị (Admin)

1. **Dashboard**
   - Xem thống kê tổng quan
   - Biểu đồ trạng thái đơn hàng
   - Top sản phẩm bán chạy
   - Đơn hàng gần đây

2. **Quản Lý Đơn Hàng**
   - Xem tất cả đơn hàng
   - Duyệt/Từ chối đơn hàng
   - Lọc theo trạng thái
   - Xem chi tiết đơn hàng

3. **Quản Lý Sản Phẩm** (Django Admin)
   - Thêm/Sửa/Xóa sản phẩm
   - Quản lý danh mục
   - Quản lý kho hàng

4. **Quản Lý Người Dùng** (Django Admin)
   - Xem danh sách người dùng
   - Quản lý vai trò (Customer/Admin)

### 🛡️ Bảo Mật

- Hash mật khẩu tự động bằng Django
- CSRF protection cho tất cả form
- Authentication required cho các chức năng nhạy cảm
- Permission-based access control

## 📁 Cấu Trúc Dự Án

```
shoe_store/
├── shoe_store/               # Project main folder
│   ├── settings.py          # Cấu hình Django
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── __init__.py
├── store/                   # Main app
│   ├── migrations/          # Database migrations
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py # Seed data command
│   ├── templates/store/     # HTML templates
│   ├── static/              # CSS, JS, images
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin config
│   ├── apps.py              # App configuration
│   └── signals.py           # Django signals
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🗄️ Cơ Sở Dữ Liệu

### Models (Bảng)

#### 1. **User (Django Built-in)**
- Quản lý thông tin đăng nhập
- Mật khẩu được hash tự động

#### 2. **UserProfile**
- Mở rộng User model
- Lưu thông tin liên hệ
- Xác định loại người dùng (Customer/Admin)

#### 3. **Category**
- Danh mục sản phẩm (Sneaker, Dép, Boot...)
- Mô tả danh mục
- Hình ảnh danh mục

#### 4. **Product**
- Chi tiết sản phẩm
- Giá, kho, đặc tính
- Đánh giá trung bình
- Mối quan hệ: 1 Category - N Products

#### 5. **Order**
- Thông tin đơn hàng
- Trạng thái (pending/approved/rejected)
- Mối quan hệ: 1 User - N Orders, 1 Product - N Orders

#### 6. **Review**
- Đánh giá sản phẩm
- Xếp hạng sao (1-5)
- Mối quan hệ: 1 Product - N Reviews, 1 User - N Reviews

### Mối Quan Hệ Dữ Liệu

```
User (1) ----< (N) UserProfile
User (1) ----< (N) Order
User (1) ----< (N) Review

Category (1) ----< (N) Product
Product (1) ----< (N) Order
Product (1) ----< (N) Review
```

## 🔗 API & URL

### Trang Công Khai

| URL | Tên Route | Chức Năng |
|-----|-----------|----------|
| `/` | home | Trang chủ |
| `/products/` | product_list | Danh sách sản phẩm |
| `/products/<id>/` | product_detail | Chi tiết sản phẩm |
| `/about/` | about | Về chúng tôi |
| `/contact/` | contact | Liên hệ |

### Xác Thực

| URL | Tên Route | Chức Năng |
|-----|-----------|----------|
| `/register/` | register | Đăng ký |
| `/login/` | login | Đăng nhập |
| `/logout/` | logout | Đăng xuất |
| `/profile/` | user_profile | Hồ sơ người dùng |

### Đơn Hàng (Yêu cầu login)

| URL | Tên Route | Chức Năng |
|-----|-----------|----------|
| `/order/create/<id>/` | create_order | Tạo đơn hàng |
| `/orders/` | order_list | Danh sách đơn hàng |
| `/orders/<id>/` | order_detail | Chi tiết đơn hàng |
| `/orders/<id>/approve/` | approve_order | Duyệt đơn (Admin) |
| `/orders/<id>/reject/` | reject_order | Từ chối đơn (Admin) |

### Đánh Giá (Yêu cầu login)

| URL | Tên Route | Chức Năng |
|-----|-----------|----------|
| `/product/<id>/review/` | add_review | Viết đánh giá |

### Dashboard & Admin (Yêu cầu Admin)

| URL | Tên Route | Chức Năng |
|-----|-----------|----------|
| `/dashboard/` | dashboard | Dashboard quản trị |
| `/admin/` | - | Django Admin |

## 📝 Phát Triển Tiếp

### Để thêm tính năng mới:

1. **Tạo model mới** trong `store/models.py`
2. **Tạo migration**: `python manage.py makemigrations`
3. **Apply migration**: `python manage.py migrate`
4. **Tạo view** trong `store/views.py`
5. **Tạo form** trong `store/forms.py` (nếu cần)
6. **Tạo template** trong `store/templates/store/`
7. **Thêm URL** trong `store/urls.py`
8. **Đăng ký model** trong `store/admin.py` (nếu cần)

## 🐛 Khắc Phục Sự Cố

### Lỗi: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Lỗi: Database
```bash
python manage.py migrate
```

### Lỗi: Static files
```bash
python manage.py collectstatic --noinput
```

### Xóa database và tạo lại
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
```

## 📚 Tài Liệu Bổ Sung

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Chart.js Documentation](https://www.chartjs.org/)

## 👨‍💻 Tác Giả

ShoeStore - Dự án học tập Django

## 📄 License

MIT License - Tự do sử dụng cho mục đích học tập

---

**Lần cập nhật cuối:** 2024
