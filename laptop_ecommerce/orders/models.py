from django.db import models
from accounts.models import Account
from products.models import MyProducts, Variations
from django.core.exceptions import ValidationError

# Create your models here.

class Payment(models.Model):
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id  = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid    = models.CharField(max_length=100)
    status         = models.CharField(max_length=100)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Addresses(models.Model):
    ADDRESS_TYPE = (
        ('Home', 'Home'),
        ('Office', 'Office'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE, default='Home')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    pincode = models.IntegerField(default=000)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Addresses, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    pincode = models.IntegerField(default=000)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name
    
class OrderProduct(models.Model):
    STATUS = (
        ('No', 'No'),
        ('Yes', 'Yes'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(MyProducts, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variations, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    requestcancel = models.CharField(max_length=30, choices=STATUS, default='No')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValidationError("Quantity cannot below zero")
        super(OrderProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.product_name
    
class Wallet(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure that the balance is not below zero
        if self.balance < 0:
            raise ValidationError("Balance cannot be below zero.")
        
        super(Wallet, self).save(*args, **kwargs)