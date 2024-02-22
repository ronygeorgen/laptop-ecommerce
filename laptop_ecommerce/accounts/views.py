from django.shortcuts import render,redirect
from django.views import View
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login , logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password


#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            print(password)

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email =  EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request,'We have sent a verification email to your email address. Please verify it.')
            return redirect ('/accounts/login/?command=verification&email='+email)
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
            
            #login for admin
            is_admin = Account.objects.filter(email=myemail, is_admin=True).exists()
            if is_admin :
                admin_details = authenticate(email=myemail, password=mypassword)
                if admin_details:
                    auth_login(request, admin_details)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid admin login credentials')
                    return redirect('login')
                
            #login for user    
            else:
                user_details = authenticate(email=myemail, password=mypassword)
                
                if user_details:
                    auth_login(request,user_details)
                    # messages.success(request, 'You are now logged in')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid login credentials')
                    return redirect('login')
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class LogoutView(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'You are logged out.')
        return redirect('login')

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None 
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'congratulations, Your account is activated.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid activation link')
            return redirect ('regiester')
        
class ForgotPasswordView(View):
    def get(self,request):
        return render (request, 'accounts/forgotPassword.html')
    def post(self,request):
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email =  EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('ForgotPassword')

class Resetpassword_ValidateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Please reset your password')
            return redirect('resetPassword')
        else:
            messages.error(request,'This link has been expired')
            return redirect('login')

class ResetPasswordView(View):
    def get(self, request):
        return render(request,'accounts/resetPassword.html')
    
    def post(self,request):
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        if check_password(new_password,user.password):
            messages.error(request, 'Choose another password')
            return redirect('resetPassword')
        elif new_password == confirm_password:
            user.password=new_password
            user.set_password(new_password)
            user.save()
            messages.success(request,'Password reset successfull')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')