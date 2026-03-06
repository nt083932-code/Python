from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Status choices for orders
STATUS_CHOICES = [
    ('pending', 'Pending Approval'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

SHOE_TYPE_CHOICES = [
    ('sneaker', 'Sneakers'),
    ('sandal', 'Sandals'),
    ('boot', 'Boots'),
    ('formal', 'Formal Shoes'),
    ('casual', 'Casual Shoes'),
]

USER_TYPE_CHOICES = [
    ('customer', 'Customer'),
    ('admin', 'Administrator'),
]


class Category(models.Model):
    """Product Category Model"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Model - Shoes and Sandals"""
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    shoe_type = models.CharField(max_length=20, choices=SHOE_TYPE_CHOICES)
    
    # Product specifications
    size = models.CharField(max_length=10, help_text="e.g., 36, 37, 38...")
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    
    # Stock and images
    quantity_in_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/', blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    
    # Ratings and reviews
    average_rating = models.FloatField(default=0, validators=[MinValueValidator(0)])
    total_reviews = models.IntegerField(default=0)
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'category']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.name} ({self.size})"

    @property
    def is_in_stock(self):
        return self.quantity_in_stock > 0


class Order(models.Model):
    """Order Model"""
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    
    # Business logic for special handling
    is_active = models.BooleanField(default=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_orders')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("can_approve_order", "Can approve orders"),
            ("can_reject_order", "Can reject orders"),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} - {self.status}"

    def calculate_total(self):
        """Calculate total price"""
        self.total_price = self.product.price * self.quantity
        return self.total_price


class Review(models.Model):
    """Product Review Model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'customer')

    def __str__(self):
        return f"Review by {self.customer.username} on {self.product.name}"


class UserProfile(models.Model):
    """Extended User Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        ordering = ['user__username']
