from django.contrib import admin
from .models import Cart, CartItem


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')



class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    list_editable = ('quantity', 'is_active')
    list_filter = ('product', 'cart', 'quantity', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)  # Register the CartItem model with the admin site
# This allows the CartItem model to be managed through the Django admin interface as well.

