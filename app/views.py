from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework import generics

from .serializers import CategorySerializer, BrandSerializer, ModelSerializer, StockSerializer, OrderSerializer
from .models import Category, Brand, Model, Stock, Order
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

class CategoryAPIView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed only.
    """
    queryset = Category.objects.all().order_by('title')
    serializer_class = CategorySerializer

class BrandAPIView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows brands to be viewed only.
    """
    queryset = Brand.objects.all().order_by('title')
    serializer_class = BrandSerializer

class ModelAPIView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows models to be viewed only.
    """
    queryset = Model.objects.all().order_by('title')
    serializer_class = ModelSerializer
    
class StockAPIView(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows stocks with is_active=True viewed only.
    """
    queryset = Stock.objects.filter(is_active=True).order_by('model')
    serializer_class = StockSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
    
    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("You cannot delete an order.")