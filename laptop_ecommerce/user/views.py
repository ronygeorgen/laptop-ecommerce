from django.shortcuts import render
from django.views import View
from products.models import MyProducts
from category.models import Category
# Create your views here.
class Home(View):
    def get(self,request):
    
        products = MyProducts.objects.all().filter(is_available=True)
        context = {
            'products' : products
        }
        return render(request,'home.html', context)
class Store(View):
    def get(self,request):
        products = MyProducts.objects.all().filter(is_available=True)
        category_list = Category.objects.all()
        product_count = products.count()
        context = {
            'products' : products,
            'product_count' : product_count,
            'category_list' : category_list,
        }
        return render(request, 'store/store.html',context)