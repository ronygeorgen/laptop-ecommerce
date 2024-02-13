from django.shortcuts import render,redirect
from django.views import View
from .models import MyProducts
from django.contrib import messages
# Create your views here.
class ProductView(View):
    templates = 'admin_templates\evara-backend\page-form-product-2.html'
    def get(self,request):
        return render (request,self.templates)
    
    def post(self,request):
        form_title          = request.POST.get('product_title')
        form_description    = request.POST.get('product_description')
        form_price          = request.POST.get('product_price')
        form_stock          = request.POST.get('product_stock')
        form_category       = request.POST.get('mycategory')
        form_image          = request.POST.get('product_image')

        if form_title and form_description and form_price and form_stock and form_category and form_image:
            product =  MyProducts(product_name=form_title, description=form_description, price=form_price, images=form_image )
            product.save()
            return redirect('Dashboard')
        messages.error(request,"Enter all fields")
        entered_data = {
            "product_name"        : form_title,
            "product_description" : form_description,
            "product_price"       : form_price,
            "product_stock"       : form_stock,
            "product_category"    : form_category,
            "product_media"       : form_image 

        }
        return render(request,self.templates, {'products' : entered_data})