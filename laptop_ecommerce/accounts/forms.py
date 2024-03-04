from django import forms
from .models import Account, UserProfile
from phonenumber_field.formfields import PhoneNumberField
import phonenumbers
import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Ensure that after "+91" there are at most 5 consecutive zeros
        national_number = phonenumbers.parse(str(phone_number), None).national_number
        if (national_number // 10) % 10**5 == 0:
            raise forms.ValidationError("After '+91', there can be at most 5 consecutive zeros.")

        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_first_name(self):

        first_name = self.cleaned_data.get('first_name')

                 
        # Check for consecutive three same letters
        if any(first_name[i] == first_name[i+1] == first_name[i+2] for i in range(len(first_name)-2)):
            raise forms.ValidationError("First name cannot contain consecutive three same letters.")

        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError("First name cannot contain digits.")
        if '.' in first_name:
            raise forms.ValidationError("First name cannot contain dots.")
        if len(first_name) <= 2:
            raise forms.ValidationError("First name must be longer than 2 characters.")
        
        return first_name
    
    def clean_last_name(self):

        last_name = self.cleaned_data.get('last_name')

        
        # Check for consecutive three same letters
        if any(last_name[i] == last_name[i+1] == last_name[i+2] for i in range(len(last_name)-2)):
            raise forms.ValidationError("Last name cannot contain consecutive three same letters.")

        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError("Last name cannot contain digits.")
        if '.' in last_name:
            raise forms.ValidationError("Last name cannot contain dots.")
        if len(last_name) <= 2:
            raise forms.ValidationError("Last name must be longer than 2 characters.")
        
        return last_name

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise forms.ValidationError("Password requires minimum 8 characters")
        

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        # Check if password contains at least one digit
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one numeric character.")

        # Check if password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")

        # Check if password contains at least one lowercase letter
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")

        # Check if password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")

        # Check for whitespaces in the password
        if ' ' in password:
            raise forms.ValidationError("Password cannot contain whitespaces.")
        
        # Check the length of the password
        
        
        return password
        
    def clean_confirmpassword(self):
        password = self.cleaned_data.get('password')
        print(password)
        confirmpassword = self.cleaned_data.get('confirmpassword')
        print(confirmpassword)

        if password is None:
        # Password did not pass the previous validation, no need to compare
            return confirmpassword

        # Check if passwords match
        if password != confirmpassword:
            raise forms.ValidationError("Passwords do not match.")
        
        return confirmpassword



    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




#===============================================================================================================================#



class UserForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean_first_name(self):

        first_name = self.cleaned_data.get('first_name')

        if not first_name.isalpha():
            raise forms.ValidationError("First name can only contain letters.")
                 
        # Check for consecutive three same letters
        if any(first_name[i] == first_name[i+1] == first_name[i+2] for i in range(len(first_name)-2)):
            raise forms.ValidationError("First name cannot contain consecutive three same letters.")

        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError("First name cannot contain digits.")
        if '.' in first_name:
            raise forms.ValidationError("First name cannot contain dots.")
        if len(first_name) <= 2:
            raise forms.ValidationError("First name must be longer than 2 characters.")
        
        return first_name
    
    def clean_last_name(self):

        last_name = self.cleaned_data.get('last_name')

        if not last_name.isalpha():
            raise forms.ValidationError("Last name can only contain letters.")
        
        # Check for consecutive three same letters
        if any(last_name[i] == last_name[i+1] == last_name[i+2] for i in range(len(last_name)-2)):
            raise forms.ValidationError("Last name cannot contain consecutive three same letters.")

        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError("Last name cannot contain digits.")
        if '.' in last_name:
            raise forms.ValidationError("Last name cannot contain dots.")
        if len(last_name) <= 2:
            raise forms.ValidationError("Last name must be longer than 2 characters.")
        
        return last_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Ensure that after "+91" there are at most 5 consecutive zeros
        national_number = phonenumbers.parse(str(phone_number), None).national_number
        if (national_number // 10) % 10**5 == 0:
            raise forms.ValidationError("After '+91', there can be at most 5 consecutive zeros.")

        return phone_number

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'Invalid':("Images only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_address_line_1(self):
        address_line_1 = self.cleaned_data['address_line_1']
        # Add your address_line_1 validation logic here
        if not address_line_1.strip():
            raise ValidationError(_("Address line 1 cannot be empty"))
        return address_line_1

    def clean_city(self):
        city = self.cleaned_data['city']
        # Add your city validation logic here
        if any(char.isdigit() for char in city):
            raise ValidationError(_("City should not contain numbers"))
        return city

    def clean_state(self):
        state = self.cleaned_data['state']
        # Add your state validation logic here
        if any(char.isdigit() for char in state):
            raise ValidationError(_("State should not contain numbers"))
        return state

    def clean_country(self):
        country = self.cleaned_data['country']
        # Add your country validation logic here
        if any(char.isdigit() for char in country):
            raise ValidationError(_("Country should not contain numbers"))
        return country