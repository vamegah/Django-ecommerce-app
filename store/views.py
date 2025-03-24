from django.shortcuts import render
from .models import Product  # Import the Product and Variation models to access product data
from django.shortcuts import get_object_or_404
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id  # Import the _cart_id function to get the cart ID from the request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Import Paginator and exceptions for pagination
from django.db.models import Q

# Create your store views here.

def store(request, category_slug=None):
    """Render the store page."""
    # This function handles the request to display the store page of the application.
    categories = None  # Initialize the categories variable to None
    products = None  # Initialize the products variable to None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)  # Retrieve the category object based on the slug
        products = Product.objects.filter(category=categories, is_available=True)  # Retrieve products belonging to the category
        paginator = Paginator(products, 6)  # Create a paginator object with 6 products per page
        page = request.GET.get('page')  # Get the current page number from the request
        paged_products = paginator.get_page(page)  # Get the products for the current page
        product_count = products.count()  # Count the number of products

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')  # Retrieve all products from the database
        paginator = Paginator(products, 6)  # Create a paginator object with 6 products per page
        page = request.GET.get('page')  # Get the current page number from the request
        paged_products = paginator.get_page(page)  # Get the products for the current page
        product_count = products.count()  # Count the number of products

    context = {
        'products': paged_products,  # Add the products to the context dictionary
        'product_count': product_count,  # Add the product count to the context dictionary
        
    }
    return render(request, 'store/store.html', context)  # Render the store.html template with the context

def product_detail(request, category_slug, product_slug):
    """Render the product detail page."""
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)  # Retrieve the product based on category and product slugs
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()  # Check if the product is in the cart


    except Exception as e:
        raise e  # Raise the exception if an error occurs

    context = {
        'single_product': single_product,  # Add the single product to the context dictionary
        'in_cart': in_cart,  # Add the in_cart flag to the context dictionary
    


    }
    return render(request, 'store/product_detail.html', context)  # Render the product_detail.html template with the context

def search(request):
    """Render the search results page."""
    # This function handles the request to display the search results based on the user's query.
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']  # Get the search keyword from the request
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))  # Search for products based on the keyword
            product_count = products.count()  # Count the number of products found
            context = {
                'products': products,  # Add the products to the context dictionary
                'product_count': product_count,  # Add the product count to the context dictionary
            }
    return render(request, 'store/store.html', context)  # Render the store.html template with the context
    
