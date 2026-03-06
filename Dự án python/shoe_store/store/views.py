from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
import json

from .models import Product, Category, Order, Review, UserProfile
from .forms import (
    UserRegisterForm, UserProfileForm, ProductFilterForm,
    OrderForm, OrderApprovalForm, ReviewForm
)


# ============== Authentication Views ==============
def register(request):
    """User Registration"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user, user_type='customer')
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'store/register.html', context)


def user_login(request):
    """User Login"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'store/login.html')


def user_logout(request):
    """User Logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# ============== Product Views ==============
def home(request):
    """Home Page - Display Featured Products"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.filter(is_active=True)
    recent_products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]

    # Dashboard statistics for admins
    dashboard_data = {}
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.user_type == 'admin':
        dashboard_data = {
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'total_customers': User.objects.count(),
            'total_revenue': sum([order.total_price for order in Order.objects.filter(status='approved')]),
        }

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'recent_products': recent_products,
        'dashboard_data': dashboard_data,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    """Product List with Search, Filter, and Sort"""
    products = Product.objects.filter(is_active=True)
    form = ProductFilterForm(request.GET or None)

    # Search
    if 'search' in request.GET and request.GET['search']:
        search_query = request.GET['search']
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    # Filter by category
    if 'category' in request.GET and request.GET['category']:
        products = products.filter(category_id=request.GET['category'])

    # Filter by price
    if 'min_price' in request.GET and request.GET['min_price']:
        try:
            min_price = float(request.GET['min_price'])
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass

    if 'max_price' in request.GET and request.GET['max_price']:
        try:
            max_price = float(request.GET['max_price'])
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass

    # Sort
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-average_rating')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'form': form,
        'category_count': Category.objects.filter(is_active=True).count(),
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    """Product Detail Page"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.reviews.filter(is_active=True).order_by('-created_at')
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk)[:4]

    user_has_ordered = False
    if request.user.is_authenticated:
        user_has_ordered = Order.objects.filter(
            customer=request.user,
            product=product,
            status='approved'
        ).exists()

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'user_has_ordered': user_has_ordered,
    }
    return render(request, 'store/product_detail.html', context)


# ============== Order Views ==============
@login_required
def create_order(request, product_id):
    """Create an Order (Place Order)"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # Check stock
            if quantity > product.quantity_in_stock:
                messages.error(request, f'Only {product.quantity_in_stock} items available.')
                return redirect('product_detail', pk=product.pk)

            order = form.save(commit=False)
            order.customer = request.user
            order.product = product
            order.calculate_total()
            order.save()

            messages.success(request, 'Order placed successfully! Waiting for admin approval.')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()

    context = {'product': product, 'form': form}
    return render(request, 'store/order_form.html', context)


@login_required
def order_list(request):
    """User's Orders List"""
    if request.user.profile.user_type == 'admin':
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Statistics
    stats = {
        'total': orders.count(),
        'pending': orders.filter(status='pending').count(),
        'approved': orders.filter(status='approved').count(),
        'rejected': orders.filter(status='rejected').count(),
    }

    context = {
        'orders': orders,
        'stats': stats,
        'status_filter': status_filter,
        'is_admin': request.user.profile.user_type == 'admin',
    }
    return render(request, 'store/order_list.html', context)


@login_required
def order_detail(request, pk):
    """Order Detail"""
    order = get_object_or_404(Order, pk=pk)

    # Check permissions
    if order.customer != request.user and request.user.profile.user_type != 'admin':
        return HttpResponseForbidden('You do not have permission to view this order.')

    if request.method == 'POST' and request.user.profile.user_type == 'admin':
        form = OrderApprovalForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.approved_by = request.user
            order.approved_date = timezone.now()
            order.save()
            messages.success(request, 'Order updated successfully.')
            return redirect('order_detail', pk=order.pk)
    elif request.user.profile.user_type == 'admin':
        form = OrderApprovalForm(instance=order)
    else:
        form = None

    context = {
        'order': order,
        'form': form,
        'is_admin': request.user.profile.user_type == 'admin',
    }
    return render(request, 'store/order_detail.html', context)


@login_required
@require_POST
def approve_order(request, pk):
    """Approve Order (Admin only)"""
    if request.user.profile.user_type != 'admin':
        return HttpResponseForbidden('You do not have permission.')

    order = get_object_or_404(Order, pk=pk)
    order.status = 'approved'
    order.approved_by = request.user
    order.approved_date = timezone.now()
    order.save()

    messages.success(request, 'Order approved successfully.')
    return redirect('order_detail', pk=order.pk)


@login_required
@require_POST
def reject_order(request, pk):
    """Reject Order (Admin only)"""
    if request.user.profile.user_type != 'admin':
        return HttpResponseForbidden('You do not have permission.')

    order = get_object_or_404(Order, pk=pk)
    order.status = 'rejected'
    order.approved_by = request.user
    order.approved_date = timezone.now()
    order.save()

    messages.success(request, 'Order rejected.')
    return redirect('order_detail', pk=order.pk)


# ============== Review Views ==============
@login_required
def add_review(request, product_id):
    """Add Product Review"""
    product = get_object_or_404(Product, pk=product_id)

    # Check if user purchased the product
    has_purchased = Order.objects.filter(
        customer=request.user,
        product=product,
        status='approved'
    ).exists()

    if not has_purchased:
        messages.error(request, 'You must purchase this product to leave a review.')
        return redirect('product_detail', pk=product.pk)

    # Check if user already reviewed
    existing_review = Review.objects.filter(product=product, customer=request.user).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = request.user
            review.is_verified_purchase = True
            review.save()

            # Update product rating
            reviews = product.reviews.filter(is_active=True)
            product.average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            product.total_reviews = reviews.count()
            product.save()

            messages.success(request, 'Review posted successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm(instance=existing_review)

    context = {
        'product': product,
        'form': form,
        'is_editing': existing_review is not None,
    }
    return render(request, 'store/review_form.html', context)


# ============== Dashboard Views ==============
@login_required
def dashboard(request):
    """Admin Dashboard"""
    if request.user.profile.user_type != 'admin':
        return redirect('home')

    # Orders data
    all_orders = Order.objects.all()
    pending_orders = all_orders.filter(status='pending')
    approved_orders = all_orders.filter(status='approved')
    rejected_orders = all_orders.filter(status='rejected')

    # Revenue calculation
    total_revenue = sum([order.total_price for order in approved_orders])
    monthly_revenue = sum([
        order.total_price for order in approved_orders
        if order.approved_date and order.approved_date.month == timezone.now().month
    ])

    # Products and categories
    top_products = Product.objects.annotate(order_count=Count('orders')).order_by('-order_count')[:5]
    total_products = Product.objects.count()
    total_categories = Category.objects.count()

    # Users
    total_users = User.objects.count()
    new_users = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()

    # Prepare chart data
    orders_by_status = {
        'pending': pending_orders.count(),
        'approved': approved_orders.count(),
        'rejected': rejected_orders.count(),
    }

    # Recent orders
    recent_orders = all_orders.order_by('-created_at')[:10]

    context = {
        'total_orders': all_orders.count(),
        'pending_orders': pending_orders.count(),
        'approved_orders': approved_orders.count(),
        'rejected_orders': rejected_orders.count(),
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
        'new_users': new_users,
        'top_products': top_products,
        'recent_orders': recent_orders,
        'orders_by_status': orders_by_status,
    }
    return render(request, 'store/dashboard.html', context)


@login_required
def user_profile(request):
    """User Profile"""
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    # Recent orders
    recent_orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]

    context = {
        'form': form,
        'profile': profile,
        'recent_orders': recent_orders,
    }
    return render(request, 'store/user_profile.html', context)


def about(request):
    """About Page"""
    return render(request, 'store/about.html')


def contact(request):
    """Contact Page"""
    return render(request, 'store/contact.html')
