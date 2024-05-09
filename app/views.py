from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework import generics

from .serializers import CategorySerializer, BrandSerializer, ModelSerializer, StockSerializer, BookingSerializer
from .models import Category, Brand, Model, Stock, Booking
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


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
    last_added_stocks = Stock.objects.filter(is_active=True).order_by('-id')[:3]
    context = {"last_added_stocks": last_added_stocks}
    return render(request, "index.html", context=context)

def products(request):
    page_title = "Products"
    products = Stock.objects.all().order_by('model')
    context = {
        "page_title": page_title,
        "products": products,
        }
    return render(request, "products.html", context=context)

def bookings(request):
    page_title = "Bookings"
    bookings = Booking.objects.all().filter(user=request.user)
    context = {
        "page_title": page_title,
        "bookings": bookings,
        }
    return render(request, "bookings.html", context=context)

def login(request):
    page_title = "Login"
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            print(request, f' welcome {username} !!')
            return redirect('index')
        else:
            print(request, f'account done not exit plz sign in')
        form = AuthenticationForm()
    else:
        return render(request, "login.html")
    
def logout(request):
    return redirect('index')

def signup(request):
    return render(request, "signup.html")

def checkout(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    return render(request, "checkout.html", context={"stock": stock})