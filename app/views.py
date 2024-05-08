from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework import generics

from .serializers import CategorySerializer, BrandSerializer, ModelSerializer, StockSerializer, BookingSerializer
from .models import Category, Brand, Model, Stock, Booking
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse, Http404

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

class BookingAPIViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)
    
    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("You cannot delete an booking.")
    
def index(request):
    last_added_stocks = Stock.objects.filter(is_active=True)[:5]
    context = {"latest_question_list": last_added_stocks}
    return render(request, "index.html", context=context)

def products(request):
    page_title = "Products"
    products = Stock.objects.all()
    context = {
        "page_title": page_title,
        "products": products,
        }
    return render(request, "products.html", context=context)

def bookings(request):
    page_title = "Products"
    bookings = Booking.objects.all().filter(user=request.user)
    context = {
        "page_title": page_title,
        "bookings": bookings,
        }
    return render(request, "bookings.html", context=context)

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def checkout(request):
    return render(request, "checkout.html")