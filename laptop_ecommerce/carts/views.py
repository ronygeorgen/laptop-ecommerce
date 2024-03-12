from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from products.models import MyProducts, Variations
from .models import *
from django.core.exceptions import ObjectDoesNotExist 
from django.http import HttpResponse
from products.models import Variations
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

class _CartId(View):
    def get(self,request):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart

class AddCartView(View):
    
    # below post method for adding product and its variation to database
    def post(self, request, variant_id):
        current_user = request.user
        variant = Variations.objects.get(id=variant_id)
        available_stock = variant.stock
        if available_stock <= 0 :
            return HttpResponse('No more stock available')
        # If the user is authenticated
        if current_user.is_authenticated:
            product_variation = self.get_variation(request, variant)

            
            # Check if the cart item already exists
            cart_item = self.get_cart_item(current_user, variant.product, product_variation)
            
            
            if cart_item:
                if available_stock > cart_item.quantity:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    return HttpResponse('Not enough stock available')
            else:
                # Create a new cart item
                cart_item = CartItem.objects.create(
                    product=variant.product,
                    quantity=1,
                    user=current_user,
                )
                cart_item.variations.add(*product_variation)
                cart_item.save()

        # If the user is not authenticated
        else:
            product_variation = self.get_variation(request, variant)

            # Get or create the cart
            cart = self.get_or_create_cart(request)

            # Check if the cart item already exists
            cart_item = self.get_cart_item(None, variant.product, product_variation, cart)
            

            if cart_item:
                # Increase the cart item quantity
                if available_stock > cart_item.quantity:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    return HttpResponse('Not enough stock available')
            else:
                # Create a new cart item
                cart_item = CartItem.objects.create(
                    product=variant.product,
                    quantity=1,
                    cart=cart,
                    
                )
                cart_item.variations.add(*product_variation)
                cart_item.save()

        return redirect('cart')

    def get_variation(self, request, variant):
        product_variation = []
        form_fields = ['product','brand_name','color', 'ram', 'storage','price','stock','description','is_active' ]
        for field in form_fields:
            value = request.POST.get(field)
            if value:
                try:
                    variation = Variations.objects.get(
                        product=variant.product,
                        brand_name=variant.brand_name, 
                        color=variant.color,
                        ram=variant.ram,
                        storage=variant.storage,
                        price=variant.price,
                        stock=variant.stock,
                        description=variant.description,
                        is_active=variant.is_active,
                        )
                    product_variation.append(variation)
                except Variations.DoesNotExist:
                    pass
        return product_variation

    def get_cart_item(self, user, product, product_variation, cart=None):
        # Check if the cart item already exists
        if user:
            return CartItem.objects.filter(product=product, user=user, variations__in=product_variation).first()
        else:
            return CartItem.objects.filter(product=product, cart=cart, variations__in=product_variation).first()

    def get_or_create_cart(self, request):
        try:
            cart_id_instance = _CartId()
            cart = Cart.objects.get(cart_id=cart_id_instance.get(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=cart_id_instance.get(request))
        cart.save()
        return cart
class RemoveCartView(View):
    def get(self, request, product_id, cart_item_id):
        cart_id_instance = _CartId()
        product = get_object_or_404(MyProducts, id=product_id)
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            else:
                cart = Cart.objects.get(cart_id= cart_id_instance.get(request)) 
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except:
            pass
        return redirect('cart')

class RemoveCartItemView(View):
    def get(self, request, product_id, cart_item_id):
        cart_id_instance = _CartId() 
        product = get_object_or_404(MyProducts, id=product_id)
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id= cart_id_instance.get(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
        return redirect('cart')

class CartView(View):
    def get(self, request):
        total = 0
        quantity = 0
        cart_items = []
        try:
            tax = 0
            grand_total = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart_id_instance = _CartId()
                cart = Cart.objects.get(cart_id=cart_id_instance.get(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.variations.first().price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax' : tax,
            'grand_total': grand_total,
        }

        return render (request, 'store/cart.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class CheckoutView(View):
    def get(self,request, total=0, quantity=0, cart_items=None):
        try:
            tax = 0
            grand_total = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart_id_instance = _CartId()
                cart = Cart.objects.get(cart_id=cart_id_instance.get(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.variations.first().price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax' : tax,
            'grand_total': grand_total,
        }
        return render(request, 'store/checkout.html', context)
 