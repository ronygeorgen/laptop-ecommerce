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
from products.models import MyProducts
from django.db.models import Sum, Count, Prefetch
from datetime import datetime
from collections import Counter
from django.utils import timezone
import calendar
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.


@method_decorator(login_required(login_url='login'), name='dispatch')
class Dashboard(View):
    def monthly_earnings(self):
        current_year = timezone.now().year
        current_month = timezone.now().month


        # Get the number of days in the current month
        _, num_days = calendar.monthrange(current_year, current_month)

        # Calculate the start and end dates for the current month
        start_date = timezone.datetime(current_year, current_month, 1)
        end_date = timezone.datetime(current_year, current_month, num_days, 23, 59, 59)

        # Calculate the total earnings for the current month
        monthly_earnings = Order.objects.filter(status=Order.status).filter(created_at__range=(start_date, end_date)).aggregate(total_earnings=Sum('order_total'))['total_earnings'] or 0
        return monthly_earnings
    def get(self,request):
        if not request.user.is_admin:
            return redirect('login')
        orders = Order.objects.filter(status='New')
        count = orders.count()

        revenue = orders.aggregate(total_revenue=Sum('order_total'))['total_revenue'] or 0

        chart_month = [0] * 12
        new_users = [0] * 12
        orders_count = [0] * 12

        for order in orders:
            month = order.created_at.month - 1
            chart_month[month] += order.order_total
            orders_count[month] += 1

        for user in Account.objects.all():
            month = user.date_joined.month - 1
            new_users[month] += 1

        all_orders = Order.objects.all().order_by('-created_at')[:10]

        date = request.GET.get('date')
        order_filter = request.GET.get('order_filter')

        if order_filter and order_filter != 'All':
            all_orders = all_orders.filter(payment__payment_status=order_filter)

        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            all_orders = all_orders.filter(created_at__date=date_obj)

        products_count = MyProducts.objects.all().count()
        categories_count = Variations.objects.values('product__category').distinct().count()

        
        # delivered_orders_with_items = orders.prefetch_related(
        #     Prefetch('orderproduct_set', queryset=OrderProduct.objects.prefetch_related('product__variations'))
        # )

        monthly_earning = self.monthly_earnings() 

        delivered_orders_with_items = orders.prefetch_related('orderproduct_set')
        delivered_product_attributes = []
        product_ids = []
        for order in delivered_orders_with_items:
            for item in order.orderproduct_set.all():
                product_ids.append(item.product.id)

        variations = Variations.objects.filter(product__id__in=product_ids)

        for variation in variations:
            delivered_product_attributes.append(variation)

        products_count = MyProducts.objects.all().count()
        categories_count = Variations.objects.values('product__category').distinct().count()
        payment_statuses = Payment.status

        product_attribute_counter = Counter(delivered_product_attributes)
        sorted_product_attributes = sorted(product_attribute_counter.items(), key=lambda x: x[1], reverse=True)


        order_products = OrderProduct.objects.filter(order__in=orders).values('variations__id', 'variations__product__product_name', 'variations__brand_name', 'variations__color', 'variations__ram', 'variations__storage', 'variations__price').annotate(count=Count('id'))
        sorted_product_attributes_for_count = sorted(order_products, key=lambda x: x['count'], reverse=True)
        context = {
        'revenue': revenue,
        'count': count,
        'orders': all_orders,
        'date': date,
        'order_filter': order_filter,
        'users': Account.objects.filter(is_admin=False).order_by('-date_joined')[:5],
        'month': chart_month,
        'new_users': new_users,
        'orders_count': orders_count,
        'payment_statuses': payment_statuses,
        'sorted_product_attributes': sorted_product_attributes,
        'monthly_earning': monthly_earning,
        'products_count': products_count,
        'categories_count': categories_count,
        'sorted_product_attributes_for_count':sorted_product_attributes_for_count,
    }


    
        return render(request, 'admin_templates/evara-backend/index.html', context) 
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
    
class OrderDetailView(View):
    def get(self, request,pk):
        selected_order = None
        try:
            selected_order = Order.objects.get(pk=pk)
        except Exception as e:
            HttpResponse(e)
        context = {
            'selected_order':selected_order,
        }
        return render(request,'admin_templates/evara-backend/page-orders-detail.html', context)
    def post(self, request, pk):
        selected_order = None
        try:
            selected_order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            # Handle case where order does not exist
            pass
        
        if selected_order:
            status = request.POST.get('status')
            if status:
                selected_order.status = status
                selected_order.save()
        
        return HttpResponseRedirect(reverse('order_detail_admin', args=[pk]))

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
    
