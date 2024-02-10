from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from . models import Category
# Create your views here.

class CategoryView(View):

    template = 'admin_templates/evara-backend/page-categories.html'

    def get(self,request):

        list_categories = Category.objects.all()
        return render(request, self.template, {'categories':list_categories})
        
    
    def post(self,request):
        
        form_category        = request.POST.get('product_name')
        form_description     = request.POST.get('product_description')
        form_category_image  = request.POST.get('cat_image')

        if form_category and form_description and form_category_image:
            category = Category(category_name = form_category, description = form_description, cat_image = form_category_image)
            category.save()
            return redirect('category')
        
        messages.error(request, 'Enter all fields')
        list_categories = Category.objects.all()
        entered_data = {
            'product_name'          : form_category,
            'product_descrption'    : form_description
        }
            
        return render(request,self.template, {'categories':list_categories, 'entered_data':entered_data})
        