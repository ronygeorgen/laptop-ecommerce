from django.shortcuts import render, get_object_or_404
from django.views import View
from products.models import MyProducts
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _CartId
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
        category_list = Category.objects.filter(is_deleted=False)
        product_count = products.count()
        context = {
            'products' : products,
            'product_count' : product_count,
            'category_list' : category_list,
        }
        return render(request, 'store/store.html',context)

class SlugStore(View):
    def get(self,request, category_slug=None):
        categories = None
        products = None
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            products = MyProducts.objects.filter(category=categories, is_available=True)
            category_list = Category.objects.filter(is_deleted=False)
            product_count = products.count()
            context = {
                'products' : products,
                'product_count' : product_count,
                'category_list' : category_list,
            }
        else: 
            products = MyProducts.objects.all().filter(is_available=True)
            category_list = Category.objects.filter(is_deleted=False)
            product_count = products.count()
            context = {
                'products' : products,
                'product_count' : product_count,
                'category_list' : category_list,
            }
        return render(request, 'store/store.html',context)

class ProductDetailView(View):
    def get(self, request, category_slug, product_slug):
        try:
            single_product = MyProducts.objects.get(category__slug=category_slug, slug=product_slug)
            cart_id_instance = _CartId()
            in_cart = CartItem.objects.filter(cart__cart_id=cart_id_instance.get(request), product=single_product).exists()
            
        except Exception as e:
            raise e
        context = {
            'single_product' : single_product,
            'in_cart'        : in_cart,
        }
        return render(request, 'store/product_detail.html', context)