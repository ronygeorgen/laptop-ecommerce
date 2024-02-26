from django.contrib import admin
from .models import MyProducts, Variations
# Register your models here.

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_values', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category','variation_values',)
admin.site.register(Variations,VariationAdmin)