from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Products
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # Orders
    path('order/create/<int:product_id>/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/approve/', views.approve_order, name='approve_order'),
    path('orders/<int:pk>/reject/', views.reject_order, name='reject_order'),

    # Reviews
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='user_profile'),

    # Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
