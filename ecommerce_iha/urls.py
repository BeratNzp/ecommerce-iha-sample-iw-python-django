"""
URL configuration for ecommerce_iha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers

from app import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryAPIView)
router.register(r'brand', views.BrandAPIView)
router.register(r'model', views.ModelAPIView)
router.register(r'stock', views.StockAPIView)
router.register(r'booking', views.BookingAPIViewSet, basename='booking')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls), name='api_v1'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('bookings', views.bookings, name='bookings'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('checkout', views.checkout, name='checkout'),
]
