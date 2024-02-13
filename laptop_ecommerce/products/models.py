from django.db import models

# Create your models here.
class MyProducts(models.Model):
    product_name        = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    description         = models.TextField(max_length=500, blank=True)
    price               = models.IntegerField()
    images              = models.ImageField(upload_to='photos/products')
    