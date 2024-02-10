from django.shortcuts import render
from django.views import View

# Create your views here.
class ProductView(View):
    templates = 'admin_templates\evara-backend\page-form-product-2.html'
    def get(self,request):
        return render (request,self.templates)