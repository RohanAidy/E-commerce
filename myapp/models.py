from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey
from mptt.fields import TreeManyToManyField

# CustomUser temporarily commented out for now
# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     postal_code = models.CharField(max_length=20, blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

class category(MPTTModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    # slug = models.SlugField(max_length=100, unique=True)  # Temporarily commented
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __str__(self):
        return self.name

class product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # slug = models.SlugField(max_length=100, unique=True)  # Temporarily commented
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='products')
    
    # Book-specific fields
    author = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True, unique=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    book_format = models.CharField(max_length=20, choices=[
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'E-book'),
        ('audiobook', 'Audiobook')
    ], default='paperback')
    genre = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} by {self.author or 'Unknown'}"

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total_price(self):
        return self.price * self.quantity

class Review(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']
