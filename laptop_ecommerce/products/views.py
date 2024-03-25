from django.shortcuts import render,redirect
from django.views import View
from .models import MyProducts, Variations, Image
from category.models import Category
from django.contrib import messages
from django.http import Http404, HttpResponse
from .forms import VariationsForm, ImageFormSet
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

# Create your views here.

def is_staff(user):
    return user.is_staff

@method_decorator(user_passes_test(is_staff), name='dispatch')
class ProductView(View):
    templates = 'admin_templates/evara-backend/page-form-product-2.html'
    def get(self,request):
        category=Category.objects.filter(is_deleted=False)
        context={
            "categorys":category,
        }
        return render (request,self.templates,context)
    
    def post(self,request):
        form_title          = request.POST.get('product_title')
        form_category       = request.POST.get('mycategory')
        # print(form_category)
        try:
            # Try to get the Category instance
            category_instance = Category.objects.get(slug=form_category)
        except Category.DoesNotExist:
            # Handle the case when the Category does not exist
            raise Http404("Category does not exist")
        
        form_isavailable    = request.POST.get('mycheck')=='True' 

        if form_title   and form_category:
            product =  MyProducts(product_name=form_title,  category=category_instance, is_available=form_isavailable)
            product.save()
            return redirect('dashboard')
        messages.error(request,"Enter all fields")
        entered_data = {
            "product_name"        : form_title,
            "product_category"    : form_category,

        }
        return render(request,self.templates, {'products' : entered_data})

@method_decorator(user_passes_test(is_staff), name='dispatch')    
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
        return render(request, 'admin_templates/evara-backend/page-product-list.html', context)

@method_decorator(user_passes_test(is_staff), name='dispatch')
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

        return render(request, 'admin_templates/evara-backend/page-form-product-2.html', context)
    def post(self, request, pk):
        product_to_be_edited = MyProducts.objects.get(pk=pk)
        product_name = request.POST.get('product_title')
        if not product_name or not product_name.strip():
            return HttpResponse("Product name should contain at least one non-whitespace character.")
        if product_name[0].isdigit():
            return HttpResponse("Product name should not start with a digit.")
        if product_name.split()[0][0].isdigit():
            return HttpResponse("Product name should not start with a digit after whitespaces.")
        product_to_be_edited.product_name = product_name
        product_to_be_edited.save()

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
        product_to_be_edited.save()
        return redirect ('product_list')

@method_decorator(user_passes_test(is_staff), name='dispatch')
class SoftDeleteProductView(View):
    def get(self, request, pk):
        product_to_delete = MyProducts.objects.get(pk=pk)
        product_to_delete.is_available = False
        product_to_delete.save()
        return redirect ('product_list')
    
#Below classes for variations 

@method_decorator(user_passes_test(is_staff), name='dispatch')
class CreateVariationFormView(View):
    template = 'admin_templates/evara-backend/variations-product-add.html'

    def get(self, request):
        variation_form = VariationsForm()
        formset = ImageFormSet()
        return render(request, self.template, {'variation_form': variation_form, 'formset': formset})

    def post(self, request):
        variation_form = VariationsForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)

        if variation_form.is_valid() and formset.is_valid():
            variation_instance = variation_form.save()
            formset.save(commit=False)
            for form in formset:
                image_instance = form.save(commit=False)
                image_instance.variation = variation_instance
                image_instance.save()
            variation_instance.save()

            return redirect('variations_list')  
        else:
            return render(request, self.template, {'variation_form': variation_form, 'formset': formset})
    
@method_decorator(user_passes_test(is_staff), name='dispatch')
class VariationsListView(View):
    def get(self, request):
        category=Category.objects.filter(is_deleted=False)
        list_variations_not_deleted   = Variations.objects.filter(is_active=True).prefetch_related('images')
        list_variations_deleted       = Variations.objects.filter(is_active=False).prefetch_related('images')
        
        context={
            "categorys": category,
            "list_variations_not_deleted" : list_variations_not_deleted,
            "list_variations_deleted" : list_variations_deleted,
        }
        return render(request,'admin_templates/evara-backend/variations-product-list.html', context)

@method_decorator(user_passes_test(is_staff), name='dispatch')
class VariationsListEditView(View):
    def get(self,request,pk):
        variant_to_edit = Variations.objects.get(pk=pk)
        variation_form = VariationsForm(instance=variant_to_edit)
        
        existing_images = variant_to_edit.images.all()
        
        # Pass the instance and queryset to ImageFormSet
        formset = ImageFormSet(instance=variant_to_edit, queryset=existing_images)
        
        # Determine the number of empty forms to display
        num_empty_forms = formset.total_form_count() - len(existing_images)
        
        # Add extra empty forms to the formset if needed
        if num_empty_forms > 0:
            formset.extra = num_empty_forms
        context = {
            'variant_to_edit': variant_to_edit,
            'variation_form': variation_form,
            'formset':formset,
        }
        return render(request, 'admin_templates/evara-backend/variations-product-add.html' ,context)
    def post(self, request, pk):
        variant_to_edit = Variations.objects.get(pk=pk)
        variation_form = VariationsForm(request.POST, instance=variant_to_edit)
        formset = ImageFormSet(request.POST, request.FILES, instance=variant_to_edit)
        if variation_form.is_valid() and formset.is_valid():
            variation_form.save()
            formset.save()
            return redirect('variations_list')
        context = {
            'variant_to_edit': variant_to_edit,
            'variation_form': variation_form,
            'formset': formset,
        }
        return render(request, 'admin_templates/evara-backend/variations-product-add.html', context)

@method_decorator(user_passes_test(is_staff), name='dispatch')
class SoftDeleteVariant(View):
    def get(self,request,pk):
        variant_to_delete = Variations.objects.get(pk=pk)
        variant_to_delete.is_active = False
        variant_to_delete.save()
        return redirect('variations_list')