from django.db import models
from category.models import Category
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class MyProducts(models.Model):
    product_name        = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    is_available        = models.BooleanField(default=False)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date         = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug       = slugify(self.product_name)
        super().save(*args, **kwargs)
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name 



class VariationsManager(models.Manager):
    def colors(self):
        return super(VariationsManager, self).filter(variation_category='color', is_active=True)
    
    def ram(self):
        return super(VariationsManager, self).filter(variation_category='ram', is_active=True)
    
    def storage(self):
        return super(VariationsManager, self).filter(variation_category='storage', is_active=True)
    

variation_category_choice = (
    ('color', 'color'),
    ('ram', 'ram'),
    ('storage', 'storage'),
)
class Variations(models.Model):
    product             = models.ForeignKey(MyProducts, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices=variation_category_choice)
    variation_values    = models.CharField(max_length=100)
    description         = models.TextField(max_length=500, blank=True)
    price               = models.IntegerField(default=0)
    stock               = models.IntegerField(default=0)
    is_active           = models.BooleanField(default=True)
    create_date         = models.DateTimeField(auto_now_add=True)

    objects = VariationsManager()

    def __str__(self):
        return self.variation_values
    
    
class Image(models.Model):
    variation = models.ForeignKey(Variations, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='static/variations')    
    