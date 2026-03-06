# 📐 Kiến Trúc Kỹ Thuật ShoeStore

## 🏗️ Tổng Quan Kiến Trúc

ShoeStore sử dụng **Model-View-Template (MVT)** architecture của Django:

```
┌─────────────────────────────────────────┐
│  Browser / Client                       │
└─────────────────────┬───────────────────┘
                      │ HTTP Request
                      ▼
┌─────────────────────────────────────────┐
│  URL Router (urls.py)                   │
│  - Định tuyến URL đến view thích hợp   │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│  Views (views.py)                       │
│  - Xử lý logic ứng dụng                │
│  - Truy vấn database                   │
│  - Xử lý form                          │
└─────────────────────┬───────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
   ┌─────────┐            ┌──────────────┐
   │ Models  │            │ Templates    │
   │ (ORM)   │            │ (HTML)       │
   └────┬────┘            └──────┬───────┘
        │                        │
        └────────────┬───────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │ Database (SQLite)        │
        │ - Categories             │
        │ - Products               │
        │ - Orders                 │
        │ - Reviews                │
        │ - Users                  │
        └──────────────────────────┘
```

---

## 📊 Model Relationships Diagram

```
┌─────────────┐          ┌──────────────┐
│   User      │          │ UserProfile  │
│  (Django)   │ 1 ━━ 1  │  (Extended)  │
│             │          │              │
│ username    │◄────────►│ phone        │
│ email       │          │ address      │
│ password    │          │ user_type    │
└──────┬──────┘          └──────────────┘
       │
       │
       │ 1 ━━━━━━ N
       │
       ▼
┌──────────────┐
│    Order     │
│              │
│ id           │
│ product_id   │
│ quantity     │
│ status       │  ◄──────┐
│ total_price  │         │
└──────┬───────┘         │
       │                 │
       └─────────────────┘
              ▲
              │ 1 ━━━━━━ N
              │
┌──────────────────────┐
│      Product         │
│                      │
│ id                   │
│ name                 │
│ price                │
│ category_id          │
│ quantity_in_stock    │
│ average_rating       │
│ image                │
└──────┬───────────────┘
       │
       │ N ━━━━━━ 1
       │
       ▼
┌──────────────────┐
│    Category      │
│                  │
│ id               │
│ name             │
│ description      │
│ image            │
└──────────────────┘

       ┌─────────────────────────────┐
       │                             │
       │ N ━━━━━━ 1 for Review       │
       │                             │
       ▼                             ▼
┌──────────────┐            ┌─────────────────┐
│    User      │            │    Product      │
│              │            │                 │
│              │ N ━ N      │    Review       │
└──────────────┘            │                 │
                            │ rating (1-5)    │
                            │ title           │
                            │ comment         │
                            └─────────────────┘
```

---

## 📁 Cấu Trúc Thư Mục Chi Tiết

```
shoe_store/                          # Root project folder
├── shoe_store/                      # Project configuration
│   ├── __init__.py
│   ├── settings.py                  # Django settings
│   │   ├── DEBUG=True
│   │   ├── INSTALLED_APPS
│   │   ├── DATABASES
│   │   ├── TEMPLATES
│   │   └── STATIC_FILES
│   ├── urls.py                      # Main URL routing
│   ├── wsgi.py                      # WSGI for deployment
│   └── asgi.py
│
├── store/                           # Main application
│   ├── migrations/                  # Database migrations
│   │   └── 0001_initial.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py         # Seed data command
│   ├── templates/
│   │   └── store/
│   │       ├── base.html            # Base template (inheritance)
│   │       ├── home.html            # Trang chủ
│   │       ├── login.html           # Đăng nhập
│   │       ├── register.html        # Đăng ký
│   │       ├── product_list.html    # Danh sách sản phẩm
│   │       ├── product_detail.html  # Chi tiết sản phẩm
│   │       ├── order_form.html      # Form đặt hàng
│   │       ├── order_list.html      # Danh sách đơn hàng
│   │       ├── order_detail.html    # Chi tiết đơn hàng
│   │       ├── dashboard.html       # Dashboard admin
│   │       ├── user_profile.html    # Hồ sơ người dùng
│   │       ├── review_form.html     # Form đánh giá
│   │       ├── about.html           # Về chúng tôi
│   │       └── contact.html         # Liên hệ
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # Custom styles
│   │   ├── js/
│   │   │   └── script.js            # JavaScript
│   │   └── images/                  # Product images
│   ├── models.py                    # Database models
│   │   ├── Category
│   │   ├── Product
│   │   ├── Order
│   │   ├── Review
│   │   └── UserProfile
│   ├── views.py                     # Business logic
│   │   ├── Authentication views
│   │   ├── Product views
│   │   ├── Order views
│   │   ├── Review views
│   │   └── Dashboard views
│   ├── forms.py                     # Django forms
│   │   ├── UserRegisterForm
│   │   ├── ProductFilterForm
│   │   ├── OrderForm
│   │   └── ReviewForm
│   ├── urls.py                      # App URL routing
│   ├── admin.py                     # Django admin config
│   ├── apps.py                      # App configuration
│   ├── signals.py                   # Django signals
│   └── __init__.py
│
├── db.sqlite3                       # SQLite database
├── manage.py                        # Django CLI
├── requirements.txt                 # Dependencies
├── .env                            # Environment variables
├── .gitignore                      # Git config
├── README.md                       # Full documentation
├── QUICK_START.md                  # Quick start guide
└── setup_db.py                     # Database setup script
```

---

## 🔄 Request/Response Flow

### 1. User Registration Flow
```
User visits /register/
       ↓
URLs routes to views.register()
       ↓
GET request → Render registration form
       ↓
User fills form and submits (POST)
       ↓
Form validation (UserRegisterForm)
       ↓
Save user to database
       ↓
Create UserProfile (via Django signal)
       ↓
Redirect to login page
```

### 2. Product Purchase Flow
```
User visits /products/<id>/
       ↓
View fetches Product from DB
       ↓
Render product_detail.html with data
       ↓
User clicks "Đặt Hàng"
       ↓
Redirect to /order/create/<id>/
       ↓
View shows OrderForm
       ↓
User enters quantity and notes
       ↓
Form validation
       ↓
Create Order with status='pending'
       ↓
Redirect to order_detail page
```

### 3. Admin Approval Flow
```
Admin logs in (/login/)
       ↓
User authenticated (Django auth)
       ↓
Access /dashboard/ (check permission)
       ↓
View queries pending orders from DB
       ↓
Display with approval buttons
       ↓
Admin clicks approve_order button
       ↓
POST to /orders/<id>/approve/
       ↓
Update order.status = 'approved'
       ↓
Set approved_date = now()
       ↓
Redirect back to order_detail
```

---

## 🔐 Security Features

### Authentication
- Django built-in `User` model
- Password hashing (PBKDF2)
- Session-based authentication
- @login_required decorator

### Authorization
- User role checking
  - admin vs customer
  - Permission decorators
- Object-level permissions
  - Users can only see their orders
  - Admins have full access

### Protection
- CSRF tokens on all forms
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- Secure password validators

---

## 📊 Database Schema (SQL View)

```sql
-- Categories
CREATE TABLE store_category (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200) UNIQUE,
    description TEXT,
    image VARCHAR(100),
    is_active BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME
);

-- Products
CREATE TABLE store_product (
    id INTEGER PRIMARY KEY,
    name VARCHAR(300),
    description TEXT,
    price DECIMAL(10,2),
    category_id INTEGER FOREIGN KEY,
    shoe_type VARCHAR(20),
    size VARCHAR(10),
    color VARCHAR(50),
    material VARCHAR(100),
    brand VARCHAR(100),
    quantity_in_stock INTEGER,
    image VARCHAR(100),
    average_rating FLOAT,
    total_reviews INTEGER,
    is_featured BOOLEAN,
    is_active BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME
);

-- Orders
CREATE TABLE store_order (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER FOREIGN KEY,
    product_id INTEGER FOREIGN KEY,
    quantity INTEGER,
    total_price DECIMAL(10,2),
    status VARCHAR(20),
    notes TEXT,
    approved_by_id INTEGER FOREIGN KEY,
    approved_date DATETIME,
    is_active BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME
);

-- Reviews
CREATE TABLE store_review (
    id INTEGER PRIMARY KEY,
    product_id INTEGER FOREIGN KEY,
    customer_id INTEGER FOREIGN KEY,
    rating INTEGER,
    title VARCHAR(200),
    comment TEXT,
    is_verified_purchase BOOLEAN,
    helpful_count INTEGER,
    is_active BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME,
    UNIQUE(product_id, customer_id)
);

-- User Profiles
CREATE TABLE store_userprofile (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE FOREIGN KEY,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    postal_code VARCHAR(20),
    user_type VARCHAR(20),
    is_active BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME
);
```

---

## 🔧 Settings Configuration

### Key Settings (settings.py)
```python
# Database
DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = 'db.sqlite3'

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'store',
    'crispy_forms',
    'django_filters',
]

# Template Settings
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'store' / 'templates']
TEMPLATES[0]['APP_DIRS'] = True

# Static & Media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Localization
LANGUAGE_CODE = 'vi-vn'
TIME_ZONE = 'Asia/Ho_Chi_Minh'

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
```

---

## 🧪 Testing & Quality

### Test Data
- 1 admin user
- 1 test customer
- 4 product categories
- 5 sample products

### Deployment Checklist
- [ ] Set DEBUG=False
- [ ] Update SECRET_KEY
- [ ] Configure DATABASE properly
- [ ] Set ALLOWED_HOSTS
- [ ] Setup HTTPS
- [ ] Collect static files
- [ ] Setup email backend
- [ ] Configure logging

---

## 📈 Performance Optimization

### Database Queries
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for reverse relations
- Index frequent lookup fields
- Use `only()` and `defer()` to limit fields

### Caching
- Cache product listings
- Cache category data
- Cache calculated fields (ratings)

### Frontend
- Minify CSS/JS
- Optimize images
- Lazy load images
- Use CDN for static files

---

## 🚀 Deployment Guide

### Option 1: Using Heroku
```bash
# Install Heroku CLI
# Create Procfile
web: gunicorn shoe_store.wsgi

# Deploy
heroku create
heroku config:set DEBUG=False
git push heroku main
```

### Option 2: Using PythonAnywhere
1. Upload files to PythonAnywhere
2. Create Python 3.9 web app
3. Configure virtual environment
4. Update settings for production

### Option 3: VPS (Ubuntu)
```bash
# Setup
sudo apt install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with Gunicorn
pip install gunicorn
gunicorn shoe_store.wsgi:application --bind 0.0.0.0:8000

# Setup Nginx as reverse proxy
```

---

## 📝 API Endpoints Summary

| Method | URL | Auth | Action |
|--------|-----|------|--------|
| GET | `/` | No | Homepage |
| GET | `/products/` | No | Product list |
| GET | `/products/<id>/` | No | Product detail |
| POST | `/register/` | No | Register user |
| POST | `/login/` | No | Login user |
| POST | `/logout/` | Yes | Logout user |
| GET | `/orders/` | Yes | My orders |
| POST | `/order/create/<id>/` | Yes | Create order |
| POST | `/orders/<id>/approve/` | Admin | Approve order |
| POST | `/product/<id>/review/` | Yes | Add review |
| GET | `/dashboard/` | Admin | Dashboard |

---

## 🎓 Learning Outcomes

Qua dự án này, bạn sẽ học được:

1. **Django Fundamentals**
   - MVT architecture
   - ORM queries
   - URL routing
   - Template system

2. **Database Design**
   - Model relationships
   - Migration management
   - Data integrity

3. **Authentication & Authorization**
   - User management
   - Session handling
   - Permission control

4. **Frontend Development**
   - Bootstrap responsive design
   - Template inheritance
   - Form handling

5. **Full Stack Development**
   - End-to-end flow
   - Security best practices
   - Deployment considerations

---

Chúc mừng! Bạn đã có một cơ sở kiến thức vững chắc về Django web development! 🚀
