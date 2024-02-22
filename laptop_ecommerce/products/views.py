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
        category=Category.objects.filter(is_deleted=False)
        context={
            "categorys":category,
        }
        return render (request,self.templates,context)
    
    def post(self,request):
        form_title          = request.POST.get('product_title')
        form_description    = request.POST.get('product_description')
        form_price          = request.POST.get('product_price')
        form_stock          = request.POST.get('product_stock')
        form_category       = request.POST.get('mycategory')
        # print(form_category)
        try:
            # Try to get the Category instance
            category_instance = Category.objects.get(slug=form_category)
        except Category.DoesNotExist:
            # Handle the case when the Category does not exist
            raise Http404("Category does not exist")
        
        form_isavailable    = request.POST.get('mycheck')=='True'
        form_image=request.FILES['product_image']  

        if form_title and form_description and form_price and form_stock and form_category and form_image:
            product =  MyProducts(product_name=form_title, description=form_description, price=form_price, stock=form_stock, category=category_instance, is_available=form_isavailable, images=form_image )
            product.save()
            return redirect('dashboard')
        messages.error(request,"Enter all fields")
        entered_data = {
            "product_name"        : form_title,
            "product_description" : form_description,
            "product_price"       : form_price,
            "product_stock"       : form_stock,
            "product_category"    : form_category,
            "product_media"       : form_image, 

        }
        return render(request,self.templates, {'products' : entered_data})
    
class ProductEdit(View):
    def get(self, request):
        category=Category.objects.filter(is_deleted=False)
        list_products_not_deleted   = MyProducts.objects.filter(is_available=True)
        list_products_deleted       = MyProducts.objects.filter(is_available=False)
        context={
            "categorys": category,
            "list_products_not_deleted" : list_products_not_deleted,
            "list_products_deleted" : list_products_deleted,
        }
        return render(request, 'admin_templates\evara-backend\page-product-list.html', context)

class ProductEditView(View):
    def get(self, request, pk):
        product_to_edit = MyProducts.objects.get(pk=pk)
        category=Category.objects.filter(is_deleted=False)
        my_id = MyProducts.objects.values('id').filter(pk=pk)
        deleted_id = MyProducts.objects.values('id').filter(pk=pk, is_available=False)
        context = {
            'product_to_edit': product_to_edit,
            "categorys": category,
            'my_id': my_id,
            'deleted_id':deleted_id,
        }

        return render(request, 'admin_templates\evara-backend\page-form-product-2.html', context)
    def post(self, request, pk):
        product_to_be_edited = MyProducts.objects.get(pk=pk)
        product_to_be_edited.product_name = request.POST.get('product_title')
        product_to_be_edited.description = request.POST.get('product_description')
        product_to_be_edited.price = request.POST.get('product_price')
        product_to_be_edited.stock = request.POST.get('product_stock')
        if 'mycategory' in request.POST:
            form_category       = request.POST.get('mycategory')
            # print(form_category)
            try:
                # Try to get the Category instance
                category_instance = Category.objects.get(slug=form_category)
            except Category.DoesNotExist:
                # Handle the case when the Category does not exist
                raise Http404("Category does not exist")
            product_to_be_edited.category = category_instance
        if 'mycheck' in request.POST:
            product_to_be_edited.is_available = request.POST.get('mycheck')=='True'
        if 'product_image' in request.FILES:
            product_to_be_edited.images = request.FILES['product_image']
        product_to_be_edited.save()
        return redirect ('product_list')

class SoftDeleteProductView(View):
    def get(self, request, pk):
        product_to_delete = MyProducts.objects.get(pk=pk)
        product_to_delete.is_available = False
        product_to_delete.save()
        return redirect ('product_list')
