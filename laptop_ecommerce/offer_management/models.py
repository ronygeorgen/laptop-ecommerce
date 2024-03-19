from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from category.models import Category
from products.models import MyProducts
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import Account
from datetime import datetime

# Create your models here.

class CategoryOffer(models.Model):
    offer_name          = models.CharField(max_length=100)
    expire_date         = models.DateField()
    category            = models.ForeignKey(Category,on_delete=models.CASCADE)
    discount_rate       = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    category_offer_slug = models.SlugField(max_length=200, unique=True)
    is_active           = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.category_offer_slug:
            self.category_offer_slug = slugify(self.offer_name)

        if self.expire_date < timezone.now().date():
            self.is_active = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.offer_name
  
    def get_absolute_url(self):
        return reverse('category_offer_detail', kwargs={'slug': self.category_offer_slug})
    
class ProductOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    expire_date = models.DateField()
    products = models.ForeignKey(MyProducts, on_delete=models.CASCADE)
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_offer_slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Automatically generate the slug from the offer name
        if not self.product_offer_slug:
            self.product_offer_slug = slugify(self.offer_name)

            if self.expire_date < timezone.now().date():
                self.is_active = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.offer_name

   