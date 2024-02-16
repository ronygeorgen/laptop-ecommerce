from django.shortcuts import render
from django.views import View
from products.models import MyProducts
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
        product_count = products.count()
        context = {
            'products' : products,
            'product_count' : product_count,
        }
        return render(request, 'store/store.html',context)