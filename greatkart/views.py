from django.shortcuts import render
from store.models import Product, ReviewRating

# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True)  # Fetch only available products
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)  # Fetch reviews for the product
    context = {
        'products': products,
        'reviews': reviews,
        } # Pass products to the template
    return render(request, 'home.html', context) # Render the home.html template with the context

