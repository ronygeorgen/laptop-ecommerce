from django.db import models
from category.models import Category
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.functions import Lower
# Create your models here.
class MyProducts(models.Model):
    product_name        = models.CharField(max_length=100, unique=True, blank=True)
    slug                = models.SlugField(max_length=200, unique=True)
    is_available        = models.BooleanField(default=False)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date         = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name



class Variations(models.Model):
    product             = models.ForeignKey(MyProducts, on_delete=models.CASCADE)
    brand_name          = models.CharField(max_length=500, blank =True)
    color               = models.CharField(max_length=100, blank=True)
    ram                 = models.CharField(max_length=100, blank=True)
    storage             = models.CharField(max_length=100, blank=True)
    price               = models.IntegerField(default=0)
    stock               = models.IntegerField(default=0)
    description         = models.TextField(max_length=500)
    is_active           = models.BooleanField(default=True)
    create_date         = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'brand_name', 'color', 'ram', 'storage', 'price', 'description')
    
    def save(self, *args, **kwargs):

        if self.price < 0:
            self.price = 0

        if self.stock < 0:
            self.stock = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.brand_name} - {self.color} - {self.ram} - {self.storage} - {self.price} - {self.description}"
    

class Image(models.Model):
    variation = models.ForeignKey(Variations, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='static/variations')    
    
    def __str__(self):
        return f"Image for {self.variation.product.product_name} -{self.variation.brand_name} - {self.variation.color} - {self.variation.ram} - {self.variation.storage}"