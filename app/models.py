from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=128)
    
    def __str__(self):
        return self.title

class Model(models.Model):
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    
class Stock(models.Model):
    model_id = models.ForeignKey(Model, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return '{' + str(self.id) + '} ' + self.model_id.brand_id.title + ' ' + self.model_id.title
    
class Order(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    stock_id = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField() # Paid for
    STATUS = {
        "PENDING": "Pending",
        "RECEIVED": "Received",
        "RETURNED": "Returned"
    }
    status = models.CharField(
        choices=STATUS,
        default=STATUS["PENDING"],
    )
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)