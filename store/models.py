from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    category = models.CharField(
        max_length=4,
        choices=[
            ('face', 'Face'),
            ('lip', 'Lip'),
            ('eye', 'Eye'),
        ],
        default='face',
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    #set image nanti

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True) # auto_now_add=True: set the date automatically when the order is created
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True) # set null: kalau productnya dihapus, order itemnya ga ikut terhapus
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) # set null: kalau order dihapus, order itemnya ga ikut terhapus
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True) # auto_now_add=True: mengatur tanggal secara otomatis
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) # set null: kalau customer dihapus, shipping addressnya ga ikut terhapus
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) # set null: kalau order dihapus, shipping addressnya ga ikut terhapus
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.address