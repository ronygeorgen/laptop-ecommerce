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