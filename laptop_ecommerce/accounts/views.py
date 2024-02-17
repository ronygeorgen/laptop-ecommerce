from django.shortcuts import render,redirect
from django.views import View
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
# from django.contrib.auth.models import a
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth.hashers import check_password

# Create your views here.
class RegisterView(View):
    def get(self,request):
        form = RegistrationForm()
        context = {
            'form' : form,
        }
        return render (request,'accounts/register.html',context)
    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['email']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            print(password)

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registration Successful')
            return redirect ('login')
        context = {
            'form' : form,
        }
        return render (request,'accounts/register.html', context)

class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated and  request.user is not None:
            return redirect('home')
       
        return render (request,'accounts/login.html')
    
    def post(self,request):
        if request.method == 'POST':
            myemail = request.POST.get('email')
            mypassword = request.POST.get('password')
            
            user_details = authenticate(email=myemail, password=mypassword)
            print(user_details)
            
            if user_details:
                auth_login(request,user_details)
                # messages.success(request, 'You are now logged in')
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('login')
        
        
class LogoutView(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')

