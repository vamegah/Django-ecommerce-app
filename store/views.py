from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
from category.models import Category

# Create your store views here.

def store(request, category_slug=None):
    """Render the store page."""
    # This function handles the request to display the store page of the application.
    categories = None  # Initialize the categories variable to None
    products = None  # Initialize the products variable to None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)  # Retrieve the category object based on the slug
        products = Product.objects.filter(category=categories, is_available=True)  # Retrieve products belonging to the category
        product_count = products.count()  # Count the number of products

    else:
        products = Product.objects.all().filter(is_available=True)  # Retrieve all products from the database
        product_count = products.count()  # Count the number of products

    context = {
        'products': products,  # Add the products to the context dictionary
        'product_count': product_count  # Add the product count to the context dictionary
    }
    return render(request, 'store/store.html', context)  # Render the store.html template with the context

def product_detail(request, category_slug, product_slug):
    """Render the product detail page."""
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)  # Retrieve the product based on category and product slugs
    except Exception as e:
        raise e  # Raise the exception if an error occurs

    context = {
        'single_product': single_product  # Add the single product to the context dictionary
    }
    return render(request, 'store/product_detail.html', context)  # Render the product_detail.html template with the context
    
