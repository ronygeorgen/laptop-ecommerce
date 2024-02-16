from django.shortcuts import render,redirect
from django.views import View
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth

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

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registration Successful')
            return redirect ('register')
        context = {
            'form' : form,
        }
        return render (request,'accounts/register.html', context)

class LoginView(View):
    def get(self,request):
        return render (request,'accounts/login.html')
    def post(self,request):
        myemail = request.POST['email']
        mypassword = request.POST['password']
        user = auth.authenticate(email=myemail, password=mypassword)
        print(user)
        if user is not None:
            auth.login(request,user)
            # messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        
class LogoutView(View):
    def get(self,request):
        return 

