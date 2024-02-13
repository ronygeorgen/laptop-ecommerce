from django.shortcuts import render,redirect
from django.views import View
from .models import MyProducts
from category.models import Category
from django.contrib import messages
from django.http import Http404 

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
        try:
            # Try to get the Category instance
            category_instance = Category.objects.get(id=form_category)
            print(category_instance)
        except Category.DoesNotExist:
            # Handle the case when the Category does not exist
            raise Http404("Category does not exist")
        
        form_image          = request.POST.get('product_image')

        if form_title and form_description and form_price and form_stock and form_category and form_image:
            product =  MyProducts(product_name=form_title, description=form_description, price=form_price, stock=form_stock, category=category_instance, images=form_image )
            product.save()
            return redirect('dashboard')
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