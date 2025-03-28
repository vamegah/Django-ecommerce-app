"""
URL configuration for greatkartecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import greatkart.views as views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    re_path(r'admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    re_path(r'^secret/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),

    path('orders/', include('orders.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# This line serves media files during development. In production, you would typically serve these files using a web server like Nginx or Apache.
# The `static()` function is used to add the URL patterns for serving media files.
