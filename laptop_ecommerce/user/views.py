from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import MyProducts, Variations, Image
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _CartId
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from carts.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
class Home(View):
    def get(self,request):
        if request.user.is_admin == True:
            return render(request,'accounts/login.html')
        else:
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
        wishlist_item = None
        try:
            single_product = MyProducts.objects.get(category__slug=category_slug, slug=product_slug)
            selected_variant = Variations.objects.get(id=variation_id)
            cart_id_instance = _CartId()
            in_cart = CartItem.objects.filter(cart__cart_id=cart_id_instance.get(request), product=single_product).exists()
            try:
                wishlist_item = WishListItems.objects.get(variantID = variation_id)
            except WishListItems.DoesNotExist:
                pass
            
        except Exception as e:
            raise e
        context = {
            'single_product' : single_product,
            'in_cart'        : in_cart,
            'selected_variant': selected_variant,
            'wishlist_item':wishlist_item,
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
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class AddToWishlistView(View):
    def get(self, request, variation_id):
        variation = Variations.objects.get(id=variation_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist_item = WishListItems.objects.create(wishlist=wishlist, variantID=variation)
        return redirect('wishlist')
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class WishlistView(View):
    def get(self,request):
        try:
            wishlist = WishList.objects.get(user=request.user.id)
        except WishList.DoesNotExist:
            wishlist = WishList.objects.create(user=request.user)
        wishlist_item = WishListItems.objects.filter(wishlist=wishlist).prefetch_related('variantID__images')
        paginator = Paginator(wishlist_item, 6)
        page = request.GET.get('page')
        paged_variations = paginator.get_page(page)
        category_list = Category.objects.filter(is_deleted=False)
        variations_count = wishlist_item.count()
        context = {
            'variations' : paged_variations,
            'variations_count' : variations_count,
            'category_list' : category_list,
        }
        return render(request, 'store/wishlist.html',context)

class RemoveWishlistView(View):
    def get(self, request, variation_id):
        variation = Variations.objects.get(id=variation_id)
        wishlist = WishList.objects.get(user=request.user)
        wishlist_item = WishListItems.objects.get(wishlist=wishlist, variantID=variation)
        wishlist_item.delete()
        wishlist = WishList.objects.get(user=request.user.id)
        wishlist_item = WishListItems.objects.filter(wishlist=wishlist).prefetch_related('variantID__images')
        paginator = Paginator(wishlist_item, 6)
        page = request.GET.get('page')
        paged_variations = paginator.get_page(page)
        category_list = Category.objects.filter(is_deleted=False)
        variations_count = wishlist_item.count()
        context = {
            'variations' : paged_variations,
            'variations_count' : variations_count,
            'category_list' : category_list,
        }
        return render(request, 'store/wishlist.html',context)

class GetVariantDetailsView(View):
    def get(self, request):
        variant_id = request.GET.get('variant_id')
        if variant_id and variant_id.isdigit():
            variant = get_object_or_404(Variations, id=variant_id)

            data = {
                'product_name': variant.product.product_name,
                'description': variant.description,
                'price': variant.price,
                'colors': [v.color for v in variant.product.variations_set.all()],
                'selected_color': variant.color,
                'rams': [v.ram for v in variant.product.variations_set.all()],
                'selected_ram': variant.ram,
                'storages': [v.storage for v in variant.product.variations_set.all()],
                'selected_storage': variant.storage,
                'currentid':variant.id,
            }
            images = [{'image_url_1': image.image.url, 'image_url_2': image.image.url} for image in variant.images.all()]
            data['images'] = images
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid or missing variant_id'}, status=400)


class GetSecondVariant(View):
    def get(self, request):
        color = request.GET.get('color')
        ram = request.GET.get('ram')
        storage = request.GET.get('storage')

        if color and ram and storage :
            try:
                variant = Variations.objects.get(
                    color=color,
                    ram=ram,
                    storage=storage
                )
                data = {
                    'product_name': variant.product.product_name,
                    'description': variant.description,
                    'price': variant.price,
                    'colors': [v.color for v in variant.product.variations_set.all()],
                    'selected_color': variant.color,
                    'rams': [v.ram for v in variant.product.variations_set.all()],
                    'selected_ram': variant.ram,
                    'storages': [v.storage for v in variant.product.variations_set.all()],
                    'selected_storage': variant.storage,
                    'currentid':variant.id,
                    
                }
                images = [{'image_url_1': image.image.url, 'image_url_2': image.image.url} for image in variant.images.all()]
                data['images'] = images

                return JsonResponse(data)

            except Variations.DoesNotExist:
                return JsonResponse({'error': 'Variant not found'}, status=404)
        else:
            return JsonResponse({'error': 'Color, RAM, or Storage is missing'}, status=400)
  