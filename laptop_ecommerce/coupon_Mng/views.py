from django.shortcuts import render
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
