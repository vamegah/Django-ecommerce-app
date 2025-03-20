from django.shortcuts import render
from store.models import Product

# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True)  # Fetch only available products
    context = {'products': products} # Pass products to the template
    return render(request, 'home.html', context) # Render the home.html template with the context

