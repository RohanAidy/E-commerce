from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import category, product, Cart, CartItem, Order, OrderItem, Review, Wishlist

@admin.register(category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    mptt_level_indent = 20
    list_filter = ('parent',)
    prepopulated_fields = {}  # Add slug field if needed later
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('tree_id', 'lft')
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Edit Book Category' if object_id else 'Add New Book Category'
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Book Categories Management'
        return super().changelist_view(request, extra_context)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_cart_items_count')
    inlines = [CartItemInline]
    
    def get_cart_items_count(self, obj):
        return obj.cartitem_set.count()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'status', 'created_at')
    search_fields = ('order_number', 'user__email')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total_price')
    search_fields = ('order__order_number', 'product__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')
    ordering = ('-added_at',)

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price', 'category', 'stock', 'featured', 'created_at')
    search_fields = ('name', 'author', 'description', 'isbn')
    list_filter = ('category', 'book_format', 'genre', 'featured', 'created_at')
    list_editable = ('price', 'stock', 'featured')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price', 'stock')
        }),
        ('Book Details', {
            'fields': ('author', 'isbn', 'publisher', 'publication_date', 'pages', 'language', 'book_format', 'genre')
        }),
        ('Media', {
            'fields': ('image', 'featured')
        }),
    )
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Edit Book' if object_id else 'Add New Book'
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Books Management'
        return super().changelist_view(request, extra_context)
