from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return str(self.username) if self.username else "No Username"
    
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
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True) # auto_now_add=True: set the date automatically when the order is created
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
       orderitems = self.orderitem_set.all()
       total = sum([item.get_total for item in orderitems])
       return total
    
    @property
    def get_cart_items(self):
       orderitems = self.orderitem_set.all()
       total = sum([item.quantity for item in orderitems])
       return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True) # set null: kalau productnya dihapus, order itemnya ga ikut terhapus
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) # set null: kalau order dihapus, order itemnya ga ikut terhapus
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True) # auto_now_add=True: mengatur tanggal secara otomatis
   
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
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
    
