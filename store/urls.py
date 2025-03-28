from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),  # This would typically point to a view that handles the store page
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),  # This handles URLs with a category slug
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),  # This handles URLs with a category and product slug
    path('search/', views.search, name='search'),  # This handles the search functionality
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),  # This handles the review submission
   
]
# This code sets up the URL routing for a Django application. It includes the URLs from the 'api' app under the 'api/' path.
# This means that any URL that starts with 'api/' will be handled by the URL configurations defined in the 'api.urls' module.