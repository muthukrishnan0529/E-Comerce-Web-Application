from django.contrib import admin
from .models import Category, products, Cart, Order, OrderItem

# ----- Category -----
admin.site.register(Category)

# ----- Products -----
class productsadmin(admin.ModelAdmin):
    list_display = ('name', 'original_price', 'selling_price', 'category', 'vendor', 'status', 'trending', 'created_at')
    list_filter = ('status', 'trending', 'category')
    search_fields = ('name', 'vendor')

admin.site.register(products, productsadmin)

# ----- Cart -----
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')

admin.site.register(Cart, CartAdmin)

# ----- OrderItems Inline -----
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price','customer_name','phone','address')
    extra = 0

# ----- Orders -----
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'total_price', 'created_at')
    search_fields = ('user__username',)

admin.site.register(Order, OrderAdmin)
