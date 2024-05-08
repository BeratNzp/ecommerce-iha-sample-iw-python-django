from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
        return self.title

class Model(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{' + str(self.id) + '} ' + self.brand.title + ' - ' + self.title
    
class Stock(models.Model):
    model = models.ForeignKey(Model, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return '{' + str(self.id) + '} ' + self.model.brand.title + ' - ' + self.model.title
    
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField() # Rented from
    end_date = models.DateTimeField() # Rented until
    STATUS = {
        "PENDING": "Pending",
        "RECEIVED": "Received",
        "DELAYED": "Delayed",
        "RETURNED": "Returned"
    }
    status = models.CharField(
        choices=STATUS,
        default=STATUS["PENDING"],
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)