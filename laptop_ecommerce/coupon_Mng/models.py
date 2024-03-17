from django.db import models
from django.utils import timezone

# Create your models here.

class Coupon(models.Model):
    coupon_id = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.end_date < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.coupon_id