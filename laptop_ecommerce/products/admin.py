from django.contrib import admin
from .models import MyProducts, Variations, Image

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','brand_name', 'color', 'ram', 'storage', 'description', 'price', 'display_images', 'stock', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'brand_name',  'color', 'ram', 'storage',)

    def display_images(self, obj):
        return ", ".join([str(image) for image in obj.images.all()])
    
    display_images.short_description = 'Images'  # Set a custom column header

admin.site.register(Variations, VariationAdmin)
admin.site.register(MyProducts)
admin.site.register(Image)