from .models import Cart, CartItem, WishList, WishListItems
from .views import _CartId
def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_id_instance = _CartId()
            cart = Cart.objects.filter(cart_id=cart_id_instance.get(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
        return dict(cart_count=cart_count)

def wishlist_counter(request):
    wishlist_count = 0
    wishlist_items = WishListItems.objects.none()
    if 'admin' in request.path:
        return {}
    else:
        if request.user.is_authenticated:

            wishlist = WishList.objects.all().filter(user=request.user)
            wishlist_items = WishListItems.objects.all().filter(wishlist=wishlist[:1])
        
        wishlist_count = wishlist_items.count()
        return dict(wishlist_count=wishlist_count)