from django.shortcuts import render, redirect, get_object_or_404  # Import the render and redirect functions to render templates and redirect to URLs
from .models import Product, ReviewRating # Import the Product and Variation models to access product data
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id  # Import the _cart_id function to get the cart ID from the request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Import Paginator and exceptions for pagination
from django.db.models import Q
from .forms import ReviewForm  # Import the ReviewForm to handle review submissions
from django.contrib import messages  # Import the messages module to display messages to the user
from orders.models import OrderProduct  # Import the OrderProduct model to check if a product is in an order
# This code defines the views for the store application. It includes functions to render the store page, product detail page, search results, and submit reviews.

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
    
    if request.user.is_authenticated:
    
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product=single_product).exists()  # Check if the product is in the order
        except OrderProduct.DoesNotExist:
            order_product = None  # Set order_product to None if the product is not in the order
    else:
        order_product = None  # Set order_product to None if the user is not authenticated

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)  # Get the reviews for the product


    context = {
        'single_product': single_product,  # Add the single product to the context dictionary
        'in_cart': in_cart,  # Add the in_cart flag to the context dictionary
        'order_product': order_product,  # Add the order_product flag to the context dictionary
        'reviews': reviews,  # Add the reviews to the context dictionary
    


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

def submit_review(request, product_id):
    """Submit a review for a product."""
    # This function handles the request to submit a review for a product.
    url = request.META.get('HTTP_REFERER')  # Get the URL of the previous page
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)  # Check if the user has already submitted a review
            form = ReviewForm(request.POST, instance=reviews)  # Create a form instance with the existing review
            form.save()  # Save the form data
            messages.success(request, 'Thank you! Your review has been updated.')  # Display a success message
            return redirect(url)  # Redirect to the previous page
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)  # Create a new form instance
            if form.is_valid():
                data = ReviewRating()  # Create a new ReviewRating object
                data.subject = form.cleaned_data['subject']  # Get the subject from the form data
                data.review = form.cleaned_data['review']  # Get the review from the form data
                data.rating = form.cleaned_data['rating']  # Get the rating from the form data
                data.ip = request.META.get('REMOTE_ADDR') # Get the IP address of the user
                product = Product.objects.get(id=product_id)  # Get the product based on the product ID
                data.product = product  # Set the product for the review
                data.user = request.user  # Set the user for the review
                data.save()  # Save the review data
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)  # Redirect to the previous page
    else:
        return redirect(url)  # Redirect to the previous page
    
