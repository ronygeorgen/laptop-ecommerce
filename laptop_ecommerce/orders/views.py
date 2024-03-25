from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem, Cart
from .forms import OrderForm
from orders.models import Order, Payment, OrderProduct, Addresses, Wallet
import datetime
import json
from products.models import MyProducts, Variations
from django.core.mail import EmailMessage
from decimal import Decimal
from django.template.loader import render_to_string
from carts.views import _CartId
from carts.utils import apply_offers


# Create your views here.
class CashOnDeliveryView(View):
    def post(self, request, order_number):
        current_user = request.user
        order = Order.objects.get(
            user=current_user, is_ordered=False, order_number=order_number
        )
        payment_method = "cod"
        payment = Payment(
            user=request.user,
            payment_id=order.order_number,
            payment_method=payment_method,
            amount_paid=order.order_total,
            status="Pending",
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()

        # Move the cart items to order product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = 0
            # Iterate over variations and get the price for each variation
            for variation in item.variations.all():
                orderproduct.product_price += variation.price

            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
            # Reduce the quantity of the sold products
            product = Variations.objects.get(id=item.variations.first().id)
            product.stock -= item.quantity
            product.save()
        # clear cart
        try:
            cart_id_instance = _CartId()
            cart = Cart.objects.filter(cart_id=cart_id_instance.get(request)).first()
            if cart and cart.coupon and cart.coupon.is_active == True:
                print("Made into false")
                cart.coupon.is_active = False
                cart.coupon.save()
        except Cart.DoesNotExist:
            pass
        cart.delete()
        CartItem.objects.filter(user=request.user).delete()
        # send order received email to customer
        mail_subject = "Thank you for your order!"
        message = render_to_string(
            "orders/order_recieved_email.html",
            {
                "user": request.user,
                "order": order,
            },
        )
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_price * i.quantity

            context = {
                "order": order,
                "ordered_products": ordered_products,
                "order_number": order.order_number,
                "transID": payment.payment_id,
                "payment": payment,
                "subtotal": subtotal,
            }
            return render(request, "orders/order_complete.html", context)
        except (Payment.DoesNotExist, Order.DoesNotExist):
            return redirect("home")


class WalletPayment(View):
    def post(self, request, order_number):
        current_user = request.user
        order = Order.objects.get(
            user=current_user, is_ordered=False, order_number=order_number
        )

        wallet = Wallet.objects.get(user=request.user)
        payment_method = "Wallet"
        payment = Payment(
            user=request.user,
            payment_id=order.order_number,
            payment_method=payment_method,
            amount_paid=order.order_total,
            status="Paid",
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        tax = order.tax
        subtotal_amount = order.order_total
        grand_total = subtotal_amount + tax
        grand_total_decimal = Decimal(str(grand_total))
        wallet.balance -= grand_total_decimal
        wallet.save()

        # Move the cart items to order product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = 0
            # Iterate over variations and get the price for each variation
            for variation in item.variations.all():
                orderproduct.product_price += variation.price

            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
            # Reduce the quantity of the sold products
            product = Variations.objects.get(id=item.variations.first().id)
            product.stock -= item.quantity
            product.save()
        # clear cart
        try:
            cart_id_instance = _CartId()
            cart = Cart.objects.filter(cart_id=cart_id_instance.get(request)).first()
            if cart and cart.coupon and cart.coupon.is_active == True:
                print("Made into false")
                cart.coupon.is_active = False
                cart.coupon.save()
        except Cart.DoesNotExist:
            pass
        cart.delete()
        CartItem.objects.filter(user=request.user).delete()
        # send order received email to customer
        mail_subject = "Thank you for your order!"
        message = render_to_string(
            "orders/order_recieved_email.html",
            {
                "user": request.user,
                "order": order,
            },
        )
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_price * i.quantity

            context = {
                "order": order,
                "ordered_products": ordered_products,
                "order_number": order.order_number,
                "transID": payment.payment_id,
                "payment": payment,
                "subtotal": subtotal,
            }
            return render(request, "orders/order_complete.html", context)
        except (Payment.DoesNotExist, Order.DoesNotExist):
            return redirect("home")


class PaymentsView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            # Store transaction detail inside Payment model
            order = Order.objects.get(
                user=request.user, is_ordered=False, order_number=body["orderID"]
            )

            # check payment method
            payment_method = body["payment_method"]

            if payment_method == "paypal":
                payment = Payment(
                    user=request.user,
                    payment_id=body["transID"],
                    payment_method=body["payment_method"],
                    amount_paid=order.order_total,
                    status=body["status"],
                )
                payment.save()

            order.payment = payment
            order.is_ordered = True
            order.save()

            # Move the cart items to order product table
            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.payment = payment
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = 0
                # Iterate over variations and get the price for each variation
                for variation in item.variations.all():
                    orderproduct.product_price += variation.price

                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()

                # Reduce the quantity of the sold products
                product = Variations.objects.get(id=item.variations.first().id)
                product.stock -= item.quantity
                product.save()

            # clear cart
            try:
                cart_id_instance = _CartId()
                cart = Cart.objects.filter(
                    cart_id=cart_id_instance.get(request)
                ).first()
                if cart and cart.coupon and cart.coupon.is_active == True:
                    print("Made into false")
                    cart.coupon.is_active = False
                    cart.coupon.save()
            except Cart.DoesNotExist:
                pass
            cart.delete()
            CartItem.objects.filter(user=request.user).delete()
            # send order received email to customer
            mail_subject = "Thank you for your order!"
            message = render_to_string(
                "orders/order_recieved_email.html",
                {
                    "user": request.user,
                    "order": order,
                },
            )
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # send order number and transaction id back to sendData method bia JsonResponse
            data = {"order_number": order.order_number, "transID": payment.payment_id}
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)})


class PlaceOrderView(View):
    def get(self, request, total=0, quantity=0):
        pass

    def post(self, request, total=0, quantity=0):
        applied_offer = None
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user)
        wallet_balance = wallet.balance
        if cart_count <= 0:
            return redirect("store")
        grand_total = 0
        tax = 0
        discount = 0
        cart_id_instance = _CartId()
        for cart_item in cart_items:
            total += cart_item.variations.first().price * cart_item.quantity

        tax = Decimal("0.02") * total
        try:
            cart_inst = Cart.objects.get(cart_id=cart_id_instance.get(request))
            if cart_inst.coupon is not None:
                discount = cart_inst.coupon.discount_rate
                grand_total = (total + tax) - discount
            else:
                grand_total = total + tax
        except Cart.DoesNotExist:
            pass
        if grand_total < 0:
            grand_total = 0
        grand_total, applied_offer = apply_offers(cart_items, grand_total)
        # store all the billing information inside the Order table
        data = Order()
        data.user = current_user
        data.first_name = request.POST.get("first_name")
        data.last_name = request.POST.get("last_name")
        data.phone = request.POST.get("phone")
        data.email = request.POST.get("email")
        data.address_line_1 = request.POST.get("address_line_1")
        data.address_line_2 = request.POST.get("address_line_2")
        data.pincode = request.POST.get("pincode")
        data.country = request.POST.get("country")
        data.state = request.POST.get("state")
        data.city = request.POST.get("city")
        data.order_note = request.POST.get("order_note")
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get("REMOTE_ADDR")
        data.save()

        # Generate order number
        yr = int(datetime.date.today().strftime("%Y"))
        dt = int(datetime.date.today().strftime("%d"))
        mt = int(datetime.date.today().strftime("%m"))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        # Check if the user wants to save the address
        save_address = request.POST.get("save_address")

        if save_address == "yes":

            address_type = request.POST.get(
                "address_type", "Home"
            )  # Default to home if not provided
            # save address to the address model
            address_data = {
                "user": current_user,
                "address_type": address_type,
                "first_name": data.first_name,
                "last_name": data.last_name,
                "phone": data.email,
                "email": data.email,
                "address_line_1": data.address_line_1,
                "address_line_2": data.address_line_2,
                "pincode": data.pincode,
                "country": data.country,
                "state": data.state,
                "city": data.city,
                "is_default": False,
            }

            address = Addresses.objects.create(**address_data)

            # now link the address to the order model
            data.address = address
            data.save()

        order = Order.objects.get(
            user=current_user, is_ordered=False, order_number=order_number
        )
        context = {
            "order": order,
            "cart_items": cart_items,
            "total": total,
            "tax": tax,
            "discount": discount,
            "grand_total": grand_total,
            "wallet_balance": wallet_balance,
            "applied_offer": applied_offer,
        }
        return render(request, "orders/payments.html", context)


class OrderCompleteView(View):
    def get(self, request):
        order_number = request.GET.get("order_number")
        transID = request.GET.get("payment_id")
        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_price * i.quantity

            # check if it's a paypal transaction
            if transID:
                payment = Payment.objects.get(payment_id=transID)
            context = {
                "order": order,
                "ordered_products": ordered_products,
                "order_number": order.order_number,
                "transID": payment.payment_id,
                "payment": payment,
                "subtotal": subtotal,
            }
            return render(request, "orders/order_complete.html", context)
        except (Payment.DoesNotExist, Order.DoesNotExist):
            return redirect("home")
