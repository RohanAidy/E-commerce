from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.core.mail import send_mail
from django.conf import settings
from .models import category, product, Cart, CartItem, Order, OrderItem, Review, Wishlist
from django.db.models import Q, Sum, Count

# Create your views here.

def home(request):
    categories = category.objects.all()
    featured_products = product.objects.filter(featured=True)[:6]
    return render(request, 'home.html', {'categories': categories, 'products': featured_products})

def category_list(request):
    categories = category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def hierarchical_categories(request):
    root_categories = category.objects.root_nodes()
    return render(request, 'hierarchical_categories.html', {'categories': root_categories})

def mptt_categories(request):
    from myapp.models import category
    
    # Get MPTT statistics
    total_categories = category.objects.count()
    root_nodes = category.objects.root_nodes().count()
    
    # Calculate max depth
    max_depth = 0
    for cat in category.objects.all():
        if cat.level > max_depth:
            max_depth = cat.level
    
    context = {
        'total_categories': total_categories,
        'root_nodes': root_nodes,
        'max_depth': max_depth + 1  # Convert to human-readable depth
    }
    
    return render(request, 'mptt_categories.html', context)

def product_list(request):
    search_query = request.GET.get('search', '')
    author_filter = request.GET.get('author', '')
    genre_filter = request.GET.get('genre', '')
    format_filter = request.GET.get('format', '')
    
    products = product.objects.all()
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    if author_filter:
        products = products.filter(author__icontains=author_filter)
    
    if genre_filter:
        products = products.filter(genre__icontains=genre_filter)
        
    if format_filter:
        products = products.filter(book_format=format_filter)
    
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product_obj = get_object_or_404(product, id=product_id)
    related_products = product.objects.filter(category=product_obj.category).exclude(id=product_id)[:4]
    reviews = Review.objects.filter(product=product_obj)
    same_author_books = product.objects.filter(author=product_obj.author).exclude(id=product_id)[:3]
    
    return render(request, 'product_detail.html', {
        'product': product_obj,
        'related_products': related_products,
        'reviews': reviews,
        'same_author_books': same_author_books
    })

def products_by_category(request, category_id):
    category_obj = get_object_or_404(category, id=category_id)
    products = product.objects.filter(category=category_obj)
    return render(request, 'products_by_category.html', {'category': category_obj, 'products': products})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        # For now, just show a simple profile page
        pass
    return render(request, 'profile.html', {'user': request.user})

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total = 0
    for item in cart_items:
        total += item.get_total_price()
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    product_obj = get_object_or_404(product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product_obj
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product_obj.name} added to cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.cart.user == request.user:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    return redirect('cart')

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product_obj = get_object_or_404(product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product_obj
    )
    
    if created:
        messages.success(request, f'{product_obj.name} added to wishlist!')
    else:
        messages.info(request, f'{product_obj.name} is already in your wishlist!')
    
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id)
    if wishlist_item.user == request.user:
        wishlist_item.delete()
        messages.success(request, 'Item removed from wishlist!')
    return redirect('wishlist')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        if name and email and subject and message:
            try:
                send_mail(
                    f'Books Store Contact: {subject}',
                    f'From: {name} ({email})\n\n{message}',
                    settings.DEFAULT_FROM_EMAIL,
                    ['admin@bookstore.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
                return redirect('contact')
            except:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'contact.html')
