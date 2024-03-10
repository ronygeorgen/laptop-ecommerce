from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from accounts.models import Account
from orders.models import Order

# Create your views here.
class Dashboard(View):
    def get(self,request):
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
        orders = Order.objects.filter(is_ordered=True)
        context = {
            'orders': orders,
        }
        return render(request, 'admin_templates/evara-backend/page-orders-1.html', context)