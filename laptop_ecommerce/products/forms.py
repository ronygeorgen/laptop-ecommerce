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
    
    
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        
    def clean_image(self):
        image = self.cleaned_data['image']
        validate_file_size(image)
        return image
ImageFormSet = forms.inlineformset_factory(Variations, Image, form=ImageForm, extra=2, can_delete=False)