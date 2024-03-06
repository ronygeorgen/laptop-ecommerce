from django.shortcuts import render, get_object_or_404
from django.views import View
from products.models import MyProducts, Variations, Image
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _CartId
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
class Home(View):
    def get(self,request):
    
        variations = Variations.objects.filter(is_active=True).distinct('product')
        context = {
            'variations' : variations
        }
        return render(request,'home.html', context)
class Store(View):
    def get(self,request):
        variations = Variations.objects.filter(is_active=True).order_by('id')
        paginator = Paginator(variations, 6)
        page = request.GET.get('page')
        paged_variations = paginator.get_page(page)
        category_list = Category.objects.filter(is_deleted=False)
        variations_count = variations.count()
        context = {
            'variations' : paged_variations,
            'variations_count' : variations_count,
            'category_list' : category_list,
        }
        return render(request, 'store/store.html',context)

class SlugStore(View):
    def get(self,request, category_slug=None):
        categories = None
        variations = None
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            variations = Variations.objects.filter(product__category=categories, is_active=True)
            
        else: 
            variations = Variations.objects.filter(is_active=True)
        paginator = Paginator(variations, 6)
        page = request.GET.get('page')
        paged_variations = paginator.get_page(page)
        category_list = Category.objects.filter(is_deleted=False)
        variations_count = variations.count()
        context = {
            'variations' : paged_variations,
            'variations_count' : variations_count,
            'category_list' : category_list,
        }
        return render(request, 'store/store.html',context)

class ProductDetailView(View):
    def get(self, request, category_slug, product_slug, variation_id):
        try:
            single_product = MyProducts.objects.get(category__slug=category_slug, slug=product_slug)
            selected_variant = Variations.objects.get(id=variation_id)
            cart_id_instance = _CartId()
            in_cart = CartItem.objects.filter(cart__cart_id=cart_id_instance.get(request), product=single_product).exists()
            
        except Exception as e:
            raise e
        context = {
            'single_product' : single_product,
            'in_cart'        : in_cart,
            'selected_variant': selected_variant,
        }
        return render(request, 'store/product_detail.html', context)
    
class SearchView(View):
    def get(self, request):
        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                variations = Variations.objects.filter(Q(product__product_name__icontains=keyword) |  Q(description__icontains=keyword) | Q(price__icontains=keyword)).order_by('-create_date')
                variations_count = variations.count()
        context = {
            'variations': variations,
            'variations_count':variations_count,
        }
        return  render(request, 'store/store.html', context)