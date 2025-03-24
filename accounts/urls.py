from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),  # This is the main cart view
    path('login/', views.login, name='login'),  # This is the main cart view
    path('logout', views.logout, name='logout'),  # This is the main cart view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
   
    
]