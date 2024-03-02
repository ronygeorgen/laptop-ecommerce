from django.contrib import admin
from .models import MyProducts, Variations

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_values', 'description', 'price', 'display_images', 'stock', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_values',)

    def display_images(self, obj):
        return ", ".join([str(image) for image in obj.images.all()])
    
    display_images.short_description = 'Images'  # Set a custom column header

admin.site.register(Variations, VariationAdmin)
admin.site.register(MyProducts)
