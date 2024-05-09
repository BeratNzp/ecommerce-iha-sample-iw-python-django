from datetime import datetime
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework import generics

from .serializers import CategorySerializer, BrandSerializer, ModelSerializer, StockSerializer, BookingSerializer
from .models import Category, Brand, Model, Stock, Booking
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

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

@login_required
def bookings(request):
    page_title = "Bookings"
    bookings = Booking.objects.all().filter(user=request.user)
    context = {
        "page_title": page_title,
        "bookings": bookings,
        }
    return render(request, "bookings.html", context=context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_url = request.POST.get('next')
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            return redirect('login')
    elif request.method == 'GET':
        page_title = "Login"
        next_url = request.POST.get('next')
        context = {
            "page_title": page_title,
        }
        if next_url:
            context['next'] = next_url
        return render(request, "login.html", context=context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return redirect('signup')
        else:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')

    elif request.method == 'GET':
        page_title = "Sign Up"
        context = {
            "page_title": page_title,
        }
        return render(request, "signup.html", context=context)
    

@login_required
def checkout(request, stock_id):
    if request.method == 'post':
        try:
            stock = Stock.objects.get(id=stock_id)
            user = request.user
            start_date = request.POST.get('start_date')
            print(start_date)
            end_date = request.POST.get('end_date')
            booking = Booking(user=user, stock=stock, start_date=start_date, end_date=end_date)
            booking.save()
            return redirect('bookings')
        except Stock.DoesNotExist:
            raise Http404("Stock does not exist")

    elif request.method == 'GET':
        stock = Stock.objects.get(id=stock_id)
        context = {
            "stock": stock,
        }
        return render(request, "checkout.html", context=context)