from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),  # This would typically point to a view that handles the store page
    path('<slug:category_slug>/', views.store, name='products_by_category'),  # This handles URLs with a category slug
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),  # This handles URLs with a category and product slug
   
]
# This code sets up the URL routing for a Django application. It includes the URLs from the 'api' app under the 'api/' path.
# This means that any URL that starts with 'api/' will be handled by the URL configurations defined in the 'api.urls' module.