from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from . models import Category
from django.http import HttpResponse
# Create your views here.

class CategoryView(View):

    template = 'admin_templates/evara-backend/page-categories.html'

    def get(self,request):

        list_categories_not_deleted = Category.objects.filter(is_deleted=False)
        list_categories_deleted     = Category.objects.filter(is_deleted=True)
        context                     = {
            'categories_not_deleted': list_categories_not_deleted,
            'categories_deleted'    :  list_categories_deleted,
        }
        return render(request, self.template, context)
        
    
    def post(self,request):
        
        form_category        = request.POST.get('product_name')
        form_description     = request.POST.get('product_description')
        form_category_image  = request.FILES.get('cat_image')

        if form_category and form_description:
            try:
                category = Category(category_name = form_category, description = form_description)
                if form_category_image:
                    category.cat_image = form_category_image
                category.save()
            except Exception as e:
                return HttpResponse(e)
            return redirect('category')
        
        messages.error(request, 'Enter all fields')
        list_categories_not_deleted = Category.objects.filter(is_deleted=False)
        list_categories_deleted     = Category.objects.filter(is_deleted=True)
        context                     = {
            'categories_not_deleted': list_categories_not_deleted,
            'categories_deleted'    :  list_categories_deleted,
            'product_name'           : form_category,
            'product_description'    : form_description
        }
            
        return render(request,self.template,context)
    

class EditView(View):
    template = 'admin_templates/evara-backend/page-categories.html'
    def get(self, request, pk):
        my_id = Category.objects.values('id').filter(pk=pk)
        print('selected id = ',my_id)
        category_to_edit = Category.objects.get(pk=pk)
        list_categories_not_deleted = Category.objects.filter(is_deleted=False)
        list_categories_deleted     = Category.objects.filter(is_deleted=True)
        deleted_id = Category.objects.values('id').filter(pk=pk, is_deleted=True)
        print('deleted id = ',deleted_id)
        context                     = {
            'category_to_edit'      : category_to_edit,
            'categories_not_deleted': list_categories_not_deleted,
            'categories_deleted'    : list_categories_deleted,
            'category'              : category_to_edit,
            'deleted_id'            : deleted_id,
            'my_id'                 : my_id,
        }
        return render(request, self.template, context)
        
    
    def post(self, request, pk):
        category_to_be_edited = Category.objects.get(pk=pk)
        category_to_be_edited.category_name = request.POST.get('product_name')
        category_to_be_edited.description = request.POST.get('product_description')
        if 'mycheck' in request.POST:
            category_to_be_edited.is_deleted    = request.POST.get('mycheck')=='False'
        if 'cat_image' in request.FILES:
            category_to_be_edited.cat_image = request.FILES['cat_image']
        category_to_be_edited.save()            
        return redirect('category')
    
class SoftDeleteCategoryView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.is_deleted = True
        category.save()
        return redirect('category')