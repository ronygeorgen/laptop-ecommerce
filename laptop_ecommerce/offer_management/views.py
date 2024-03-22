from django.shortcuts import render, redirect
from django.views import View
from .forms import CategoryOfferForm, ProductOfferForm
from category.models import Category
from products.models import MyProducts
from .models import CategoryOffer, ProductOffer
from django.http import Http404, HttpResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

# Create your views here.
def is_staff(user):
    return user.is_staff

class CategoryOfferView(View):
    def get(self, request):
        form = CategoryOfferForm()
        active_category_offer = CategoryOffer.objects.filter(is_active=True)
        deactive_category_offer = CategoryOffer.objects.filter(is_active=False)
        context = {
            "form": form,
            "active_category_offer": active_category_offer,
            "deactive_category_offer": deactive_category_offer,
        }
        return render(
            request,
            "admin_templates/evara-backend/page-category-offer-mng.html",
            context,
        )

    def post(self, request):
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            offer_name = form.cleaned_data["offer_name"]
            expire_date = form.cleaned_data["expire_date"]
            category = form.cleaned_data["category"]
            discount_rate = form.cleaned_data["discount_rate"]
            is_active = form.cleaned_data["is_active"]

            category_offer = CategoryOffer.objects.create(
                offer_name=offer_name,
                expire_date=expire_date,
                category=category,
                discount_rate=discount_rate,
                is_active=is_active,
            )
            category_offer.save()
        return redirect("category_offer")

@method_decorator(user_passes_test(is_staff), name='dispatch')
class CategoryEditView(View):
    def get(self, request, pk):
        my_id = CategoryOffer.objects.values("id").filter(pk=pk)
        category_offer_to_edit = CategoryOffer.objects.get(pk=pk)
        form = CategoryOfferForm(instance=category_offer_to_edit)
        try:
            deleted_id = CategoryOffer.objects.values("id").filter(
                pk=pk, is_active=False
            )
        except CategoryOffer.DoesNotExist:
            pass
        active_category_offer = CategoryOffer.objects.filter(is_active=True)
        deactive_category_offer = CategoryOffer.objects.filter(is_active=False)
        context = {
            "category": category_offer_to_edit,
            "active_category_offer": active_category_offer,
            "deactive_category_offer": deactive_category_offer,
            "form": form,
            "my_id": my_id,
            "deleted_id": deleted_id,
        }
        return render(
            request,
            "admin_templates/evara-backend/page-category-offer-mng.html",
            context,
        )

    def post(self, request, pk):
        category_to_be_edited = CategoryOffer.objects.get(pk=pk)
        form = CategoryOfferForm(request.POST, instance=category_to_be_edited)
        if form.is_valid():
            category_to_be_edited = form.save(commit=False)
            category_to_be_edited.offer_name = form.cleaned_data["offer_name"]
            category_to_be_edited.expire_date = form.cleaned_data["expire_date"]

            # Check if 'category' is in the cleaned_data
            if "category" in form.cleaned_data:
                form_category = form.cleaned_data["category"]
                # Convert the category input to a slug
                category_slug = slugify(form_category)
                try:
                    # Try to get the Category instance based on the slug
                    category_instance = Category.objects.get(slug=category_slug)
                except CategoryOffer.DoesNotExist:
                    # Handle the case when the Category does not exist
                    raise HttpResponse("Category does not exist")
                category_to_be_edited.category = category_instance

            category_to_be_edited.discount_rate = form.cleaned_data["discount_rate"]
            value = category_to_be_edited.is_active
            # Check if 'is_active' is in the cleaned_data
            if category_to_be_edited.is_active == False:
                category_to_be_edited.is_active = True

            category_to_be_edited.save()
            return redirect("category_offer")
        else:
            my_id = CategoryOffer.objects.values("id").filter(pk=pk)
            category_offer_to_edit = CategoryOffer.objects.get(pk=pk)
            try:
                deleted_id = CategoryOffer.objects.values("id").filter(
                    pk=pk, is_active=False
                )
            except CategoryOffer.DoesNotExist:
                pass
            active_category_offer = CategoryOffer.objects.filter(is_active=True)
            deactive_category_offer = CategoryOffer.objects.filter(is_active=False)
            context = {
                "category": category_offer_to_edit,
                "active_category_offer": active_category_offer,
                "deactive_category_offer": deactive_category_offer,
                "form": form,
                "my_id": my_id,
                "deleted_id": deleted_id,
            }
        return render(
            request,
            "admin_templates/evara-backend/page-category-offer-mng.html",
            context,
        )

@method_decorator(user_passes_test(is_staff), name='dispatch')
class SoftDeleteCategoryOfferView(View):
    def get(self, request, pk):
        category = CategoryOffer.objects.get(pk=pk)
        category.is_active = False
        category.save()
        return redirect("category_offer")


# ------------------------------------------------------------------------#


# Product offer
@method_decorator(user_passes_test(is_staff), name='dispatch')
class ProductOfferView(View):
    def get(self, request):
        form = ProductOfferForm()
        active_product_offer = ProductOffer.objects.filter(is_active=True)
        deactive_product_offer = ProductOffer.objects.filter(is_active=False)
        context = {
            "form": form,
            "active_product_offer": active_product_offer,
            "deactive_product_offer": deactive_product_offer,
        }
        return render(
            request,
            "admin_templates/evara-backend/page-product-offer-mng.html",
            context,
        )

    def post(self, request):
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            offer_name = form.cleaned_data["offer_name"]
            expire_date = form.cleaned_data["expire_date"]
            products = form.cleaned_data["products"]
            discount_rate = form.cleaned_data["discount_rate"]
            is_active = form.cleaned_data["is_active"]

            product_offer = ProductOffer.objects.create(
                offer_name=offer_name,
                expire_date=expire_date,
                products=products,
                discount_rate=discount_rate,
                is_active=is_active,
            )
            product_offer.save()
        return redirect("product_offer")

@method_decorator(user_passes_test(is_staff), name='dispatch')
class ProductEditView(View):
    def get(self, request, pk):
        my_id = ProductOffer.objects.values("id").filter(pk=pk)
        product_offer_to_edit = ProductOffer.objects.get(pk=pk)
        form = ProductOfferForm(instance=product_offer_to_edit)
        try:
            deleted_id = ProductOffer.objects.values("id").filter(
                pk=pk, is_active=False
            )
        except ProductOffer.DoesNotExist:
            pass
        active_product_offer = ProductOffer.objects.filter(is_active=True)
        deactive_product_offer = ProductOffer.objects.filter(is_active=False)
        context = {
            "product": product_offer_to_edit,
            "active_product_offer": active_product_offer,
            "deactive_product_offer": deactive_product_offer,
            "form": form,
            "my_id": my_id,
            "deleted_id": deleted_id,
        }
        return render(
            request,
            "admin_templates/evara-backend/page-product-offer-mng.html",
            context,
        )

    def post(self, request, pk):
        product_to_be_edited = ProductOffer.objects.get(pk=pk)
        form = ProductOfferForm(request.POST, instance=product_to_be_edited)
        if form.is_valid():
            product_to_be_edited = form.save(commit=False)
            product_to_be_edited.offer_name = form.cleaned_data["offer_name"]
            product_to_be_edited.expire_date = form.cleaned_data["expire_date"]
            if "products" in form.cleaned_data:
                form_products = form.cleaned_data["products"]
                product_slug = slugify(form_products)
                try:
                    product_instance = MyProducts.objects.get(slug=product_slug)
                    print("product instance = ", product_instance)
                except MyProducts.DoesNotExist:
                    raise HttpResponse("Product does not exist")
                product_to_be_edited.products = product_instance

            product_to_be_edited.discount_rate = form.cleaned_data["discount_rate"]
            if product_to_be_edited.is_active == False:
                product_to_be_edited.is_active = True

            product_to_be_edited.save()
            return redirect("product_offer")
        else:
            my_id = ProductOffer.objects.values("id").filter(pk=pk)
            product_offer_to_edit = ProductOffer.objects.get(pk=pk)
            try:
                deleted_id = ProductOffer.objects.values("id").filter(
                    pk=pk, is_active=False
                )
            except ProductOffer.DoesNotExist:
                pass
            active_product_offer = ProductOffer.objects.filter(is_active=True)
            deactive_product_offer = ProductOffer.objects.filter(is_active=False)
            context = {
                "product": product_offer_to_edit,
                "active_product_offer": active_product_offer,
                "deactive_product_offer": deactive_product_offer,
                "form": form,
                "my_id": my_id,
                "deleted_id": deleted_id,
            }

            return render(
                request,
                "admin_templates/evara-backend/page-product-offer-mng.html",
                context,
            )

@method_decorator(user_passes_test(is_staff), name='dispatch')
class SoftDeleteProductOfferView(View):
    def get(self, request, pk):
        product = ProductOffer.objects.get(pk=pk)
        product.is_active = False
        product.save()
        return redirect("product_offer")
