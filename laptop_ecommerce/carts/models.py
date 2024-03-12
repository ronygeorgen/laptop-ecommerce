from django.db import models
from products.models import MyProducts, Variations
from accounts.models import Account

# Create your models here.

class Cart(models.Model):
    cart_id     = models.CharField(max_length=250, blank=True)
    date_added  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user        = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product     = models.ForeignKey(MyProducts, on_delete=models.CASCADE)
    variations  = models.ManyToManyField(Variations, blank=True)
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity    = models.IntegerField()
    is_active   = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
    
class WishList(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"WishList {self.id} - User: {self.user.username}"

class WishListItems(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    variantID = models.ForeignKey(Variations, on_delete=models.CASCADE)

    def __str__(self):
        return f"WishListItems {self.id} - WishList: {self.wishlist.id}, VariantID: {self.variantID}"
