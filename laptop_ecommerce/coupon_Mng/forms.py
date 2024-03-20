from django import forms 
from . models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_id', 'end_date', 'discount_rate']
        widgets = {
            'coupon_id' : forms.TextInput(attrs={'class':'form-control'}),
            'end_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'discount_rate': forms.NumberInput(attrs={'class':'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        coupon_id = cleaned_data.get('coupon_id')
        end_date = cleaned_data.get('end_date')
        discount_rate = cleaned_data.get('discount_rate')

        if not coupon_id or not end_date or not discount_rate:
            raise forms.ValidationError("All fields are required.")

        return cleaned_data