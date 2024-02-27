from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from products.models import MyProducts
from .models import *
from django.core.exceptions import ObjectDoesNotExist 
from django.http import HttpResponse
from products.models import Variations
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class _CartId(View):
    def get(self,request):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart

class AddCartView(View):
    def get(self, request, product_id):
        product = MyProducts.objects.get(id=product_id) #get the product
        try:
            cart_id_instance = _CartId()
            cart = Cart.objects.get(cart_id= cart_id_instance.get(request)) #get the cart using the cart id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = cart_id_instance.get(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()

        return redirect ('cart')
    
    # below post method for adding product and its variation to database
    def post(self, request, product_id):
        current_user = request.user
        product = MyProducts.objects.get(id=product_id) #get the product
        # if the user authenticated
        if current_user.is_authenticated:
            product_variation = []
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variations.objects.get(product=product, variation_category__iexact = key, variation_values__iexact = value)
                    product_variation.append(variation)
                except:
                    pass

            # below variations grouping happens
            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, user=current_user)
                existing_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    existing_var_list.append(list(existing_variation))
                    id.append(item.id)

                if product_variation in existing_var_list:
                    # increase the cart item quantity
                    index = existing_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()
                else:
                    # create the cart item
                    item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user = current_user,
                )
                if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                cart_item.save()

            return redirect ('cart')
        # if the user is not authenticated
        else:
            product_variation = []
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variations.objects.get(product=product, variation_category__iexact = key, variation_values__iexact = value)
                    product_variation.append(variation)
                except:
                    pass

            
            try:
                cart_id_instance = _CartId()
                cart = Cart.objects.get(cart_id= cart_id_instance.get(request)) #get the cart using the cart id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = cart_id_instance.get(request)
                )
            cart.save()

            # below variations grouping happens
            is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.filter(product=product, cart=cart)
                #   existing_variation -> coming database
                #   current_variation  -> coming from the variable product_variation
                #   item_id  -> coming from database
                existing_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    existing_var_list.append(list(existing_variation))
                    id.append(item.id)

                if product_variation in existing_var_list:
                    # increase the cart item quantity
                    index = existing_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()
                else:
                    # create the cart item
                    item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                    if len(product_variation) > 0:
                        item.variations.clear()
                        item.variations.add(*product_variation)
                    item.save()
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
                if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                cart_item.save()

            return redirect ('cart')

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
    def get(self, request, total=0, quantity=0, cart_items=None):
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
                total += (cart_item.product.price * cart_item.quantity)
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
                total += (cart_item.product.price * cart_item.quantity)
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