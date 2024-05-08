from django.contrib import admin
from .models import Category, Brand, Model, Stock, Booking

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Stock)
admin.site.register(Booking)