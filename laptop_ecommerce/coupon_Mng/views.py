from django.shortcuts import render, redirect
from django.views import View
from .models import Coupon
from .forms import CouponForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
# Create your views here.

class AddCoupon(View):
    def get(self,request):
        coupons = Coupon.objects.all()
        expired_coupons = Coupon.objects.filter(is_active=True, end_date__lt=timezone.now())
        for coupon in expired_coupons:
            coupon.is_active=False
            coupon.save()
        form = CouponForm()
        context = {
            'form': form,
            'coupons': coupons,
        }
        return render(request, 'admin_templates/evara-backend/coupon_mng.html', context)
    def post(self,request):
        coupons = Coupon.objects.all()
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon added successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            form = CouponForm()
            context = {
                'form': form,
                'coupons': coupons,
            }
            return render(request, 'admin_templates/evara-backend/coupon_mng.html', context)

class EditCouponView(View):
    def get(self,request,pk):
        coupon_to_edit = Coupon.objects.get(pk=pk)
        form = CouponForm( instance=coupon_to_edit)
        coupons = Coupon.objects.all()
        expired_coupons = Coupon.objects.filter(is_active=True, end_date__lt=timezone.now())
        for coupon in expired_coupons:
            coupon.is_active=False
            coupon.save()
        context = {
            'coupon_to_edit': coupon_to_edit,
            'form': form,
            'coupons': coupons,
        }
        return render(request, 'admin_templates/evara-backend/coupon_mng.html', context)
    def post(self,request,pk):
        coupon_to_edit = Coupon.objects.get(pk=pk)
        form = CouponForm(request.POST, instance=coupon_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon edited successfully')
            return redirect('add_coupon')
        else:
            coupons = Coupon.objects.all()
            context = {
                'coupon_to_edit': coupon_to_edit,
                'form': form,
                'coupons': coupons,
            }
            return render(request, 'admin_templates/evara-backend/coupon_mng.html', context)

class DeleteCouponView(View):
    def get(self,request,pk):
        coupon_to_delete = Coupon.objects.get(pk=pk)
        coupon_to_delete.delete()
        return redirect('add_coupon')