from django.contrib import admin
from .models import Product, Variation

# Register your models here.
# Register the Product model with the Django admin site
# This allows the Product model to be managed through the Django admin interface.
class ProductAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Product model.
    """
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    # This line specifies that the 'slug' field should be automatically populated with the 'product_name' field.
    # This is useful for creating unique URLs for each product.

# Register the Product model with the customized ProductAdmin class
admin.site.register(Product, ProductAdmin)
# This code registers the Product model with the Django admin site, allowing it to be managed through the admin interface.

class VariationAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Variation model.
    """
    list_display = ('product', 'variation_category', 'variation_value', 'variation_image', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'variation_image',)

admin.site.register(Variation, VariationAdmin) # Register the Variation model with the admin site
# This allows the Variation model to be managed through the Django admin interface as well.
