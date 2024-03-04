from django import forms
from .models import Variations, Image
from multiupload.fields import MultiFileField 
from django.core.exceptions import ValidationError

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5MB limit in bytes
    if value.size > limit:
        raise ValidationError('Uploaded file exceeds the maximum size of 5MB.')


class VariationsForm(forms.ModelForm):
    class Meta:
        model = Variations
        fields = ['product', 'variation_category', 'variation_values', 'description', 'price', 'stock', 'is_active']

    def __init__(self, *args, **kwargs):
        super(VariationsForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['class'] = 'form-control'
        self.fields['variation_category'].widget.attrs['class'] = 'form-control'
        self.fields['variation_values'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['class'] = 'form-control'
    
    
    
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

        
        
    def clean_image(self):
        image = self.cleaned_data['image']
        validate_file_size(image)
        self.validate_image_content(image)
        return image
    
    def validate_image_content(self, image):
        # Custom validation for the 'image' field
        if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise ValidationError('Only image files (PNG, JPG, JPEG, GIF) are allowed.')
        
ImageFormSet = forms.inlineformset_factory(Variations, Image, form=ImageForm, extra=2, can_delete=False)