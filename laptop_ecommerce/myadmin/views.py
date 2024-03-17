from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from accounts.models import Account
from products.models import Variations
from orders.models import Order, OrderProduct, Wallet, Payment
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required(login_url='login'), name='dispatch')
class Dashboard(View):
    def get(self,request):
        if not request.user.is_admin:
            return redirect('login')
        return render(request,'admin_templates/evara-backend/index.html')
class UserManagementView(View):
    def get(self, request):
        active_users_list = Account.objects.filter(is_active=True, is_admin=False)
        blocked_users_list = Account.objects.filter(is_active=False, is_admin=False)
        context = {
            'active_users_list': active_users_list,
            'blocked_users_list': blocked_users_list,
        }
        return render (request, 'admin_templates/evara-backend/user-list.html', context)

class UserBlockView(View):
    def get(self, request, pk):
        user_to_be_blocked = Account.objects.get(pk=pk)
        user_to_be_blocked.is_active = False
        user_to_be_blocked.save()
        return redirect('user_list')
        
class UserUnblockView(View):
    def get(self, request, pk):
        user_to_be_unblocked = Account.objects.get(pk=pk)
        user_to_be_unblocked.is_active = True
        user_to_be_unblocked.save()
        return redirect('user_list')
    
class OrderList(View):
    def get(self, request):
        orders = OrderProduct.objects.filter(ordered=True).order_by('-created_at')
        cancel_requests = [order for order in orders if order.requestcancel == 'Yes']

        context = {
            'orders': orders,
            'cancel_requests': cancel_requests,
        }
        return render(request, 'admin_templates/evara-backend/page-orders-1.html', context)

class OrderCancelApprove(View):
    def post(self,request,pk):
        try:
            order = OrderProduct.objects.get(pk=pk)
            # order.ordered='False'
            # order.quantity -= 1
            order.requestcancel ='No'
            order.is_cancelled = True
            # order.order.status = 'Cancelled'
            # order.order.is_ordered = False
            # order.payment.status = 'Cancelled'
            order.save()
            for variation in order.variations.all():
                    variation.stock += 1
                    variation.save()

        except OrderProduct.DoesNotExist:
            pass

        user_instance = order.user
        try:
            payment = Payment.objects.filter(user=user_instance, payment_id=order.order.order_number , payment_method='cod').first()
            
            if not payment:
                try:
                    wallet = Wallet.objects.get(user=user_instance)
                    wallet.balance += Decimal(order.product_price)
                    wallet.save()
                except Wallet.DoesNotExist:
                    wallet = Wallet(
                        user=user_instance,
                        balance=order.product_price,
                    )
                    wallet.save()
        except Payment.DoesNotExist:
            pass
        
        return redirect('order_list')

class SalesReportView(View):
    def get(self, request):
        if not request.user.is_admin:
            return redirect('login')

        start_date_value = ""
        end_date_value = ""
        try:
            orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
        except:
            pass

        context = {
            'orders': orders,
            'start_date_value': start_date_value,
            'end_date_value': end_date_value
        }

        return render(request, 'admin_templates/evara-backend/sales_report.html', context)

    def post(self, request):
        if not request.user.is_admin:
            return redirect('adminlog:admin_login')

        start_date_value = ""
        end_date_value = ""
        orders = Order.objects.filter(is_ordered=True).order_by('-created_at')

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            orders = orders.filter(created_at__range=(start_date, end_date))

        context = {
            'orders': orders,
            'start_date_value': start_date_value,
            'end_date_value': end_date_value
        }

        return render(request, 'admin_templates/evara-backend/sales_report.html', context)