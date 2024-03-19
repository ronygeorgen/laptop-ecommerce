from django import forms
from .models import CategoryOffer, ProductOffer

class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ['offer_name', 'expire_date', 'category', 'discount_rate', 'is_active']

    def __init__(self, *args, **kwargs):
        super(CategoryOfferForm, self).__init__(*args, **kwargs)
        placeholders = {
            'offer_name': 'Enter offer name',
            'expire_date': 'YYYY-MM-DD',
            'category': 'Select category',
            'discount_rate': 'Enter discount rate',
        }
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
        self.fields['is_active'].widget.attrs['class'] = ' form-check-input'

    def clean_discount_rate(self):
        discount_rate = self.cleaned_data['discount_rate']
        if discount_rate > 999.00:
            raise forms.ValidationError("Discount rate cannot be greater than 999.00")
        return discount_rate

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['offer_name', 'expire_date', 'products', 'discount_rate', 'is_active']

    def __init__(self, *args, **kwargs):
        super(ProductOfferForm, self).__init__(*args, **kwargs)
        placeholders = {
            'offer_name': 'Enter offer name',
            'expire_date': 'YYYY-MM-DD',
            'products': 'Select product',
            'discount_rate': 'Enter discount rate',
        }
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
        self.fields['is_active'].widget.attrs['class'] = ' form-check-input'

    def clean_discount_rate(self):
        discount_rate = self.cleaned_data['discount_rate']
        if discount_rate > 999.00:
            raise forms.ValidationError("Discount rate cannot be greater than 999.00")
        return discount_rate