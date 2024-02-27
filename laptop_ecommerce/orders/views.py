from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from carts.models  import CartItem, Cart
from .forms import OrderForm
from orders.models import Order, Payment
import datetime
import json
# Create your views here.

class PaymentsView(View):
    def post(self, request):
        body = json.loads(request.body)
        # Store transaction detail inside Payment model
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
        payment = Payment(
            user = request.user,
            payment_id = body['transID'],
            payment_method = body['payment_method'],
            amount_paid = order.order_total,
            status = body['status'],
        )

        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()
        
        #Move the cart items to order product table
        
        #Reduce the quantity of the sold products

        #clear cart

        #send order received email to customer

        #send order number and transaction id back to sendData method bia JsonResponse

        return render (request, 'orders/payments.html')


class PlaceOrderView(View):
    def get(self, request, total=0, quantity=0):
        current_user = request.user

        #if the cart count is less than or equal to zero, then redirect back to shop
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <= 0 :
            return redirect('store')

        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity = cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        return HttpResponse('Currently working code in orders/views.py. PlaceOrderView class get function')
    
    def post(self, request, total=0, quantity=0):
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <= 0 :
            return redirect('store')
        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity = cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        #store all the billing information inside the Order table
        data = Order()
        data.user = current_user
        data.first_name = request.POST.get('first_name')
        data.last_name = request.POST.get('last_name')
        data.phone = request.POST.get('phone')
        data.email = request.POST.get('email')
        data.address_line_1 = request.POST.get('address_line_1')
        data.address_line_2 = request.POST.get('address_line_2')
        data.pincode = request.POST.get('pincode')
        data.country = request.POST.get('country')
        data.state = request.POST.get('state')
        data.city = request.POST.get('city')
        data.order_note = request.POST.get('order_note')
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()

        #Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total
        }
        return render(request, 'orders/payments.html',context)
