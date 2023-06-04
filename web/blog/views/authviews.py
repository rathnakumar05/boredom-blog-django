from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.signing import dumps, loads
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string

from ..forms.authform import RegisterForm, LoginForm, ForgotPasswordForm, ForgotPasswordChangeForm
from ..utils.decorators import anonymous_required, not_verified
from ..models import User

class RegisterView(View):

    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'blog/auth/register.html', { 'form' : form })
    
    @method_decorator(anonymous_required)
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.instance.role = "USER"
            user = form.save()
            login(request, user)
            request.session["is_verified"] = False
            email = str(form.instance.email)
            token = dumps(email)
            link = get_current_site(request).domain + reverse('verify-token') + "?q=" + token
            subject = 'Confirmation Email'
            message = f"verification link <a href='{link}'>Verify</a>"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ email ]
            send_mail( subject, message, email_from, recipient_list )
            return redirect("home")
        return render(request, 'blog/auth/register.html', { 'form' : form })
    
class LoginView(View):

    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'blog/auth/login.html', { 'form' : form })
    
    @method_decorator(anonymous_required)
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                request.session["is_verified"] = user.is_verified
                if request.GET.get("next") is not None:
                    return redirect(request.GET.get("next"))
                return redirect("home")
            else:
                form.non_field_errors = ["Invalid credentials"]
        return render(request, 'blog/auth/login.html', { 'form' : form })
    
class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
    
class SendVerifyView(View):
    @method_decorator(login_required)
    @method_decorator(not_verified)
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/auth/verify.html')
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        email = str(request.user)
        token = dumps(email)
        link = get_current_site(request).domain + reverse('verify-token') + "?q=" + token
        subject = 'Confirmation Email'
        message = f"verification link <a href='{link}'>Verify</a>"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [ email ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request, 'blog/auth/verify.html')
    
class VerifyView(View):

    def get(self, request, *args, **kwargs):
        token = request.GET.get("q")
        if token is not None:
            try:
                email = loads(token, max_age=3600)
                user = User.objects.get(email=email)
                if user:
                    user.is_verified = True
                    user.save()
                    login(request, user)
                    request.session["is_verified"] = user.is_verified
                    return redirect("home")
            except:
                data = None
        return HttpResponse("Verification link expired")
    
class ForgotPasswordView(View):
    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        form = ForgotPasswordForm()
        return render(request, 'blog/auth/forgot-password.html', { 'form' : form })
    
    @method_decorator(anonymous_required)
    def post(self, request, *args, **kwargs):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            user = User.objects.get(email=email)
            if user:
                reset_token = get_random_string(length=32)
                user.reset_token = reset_token
                user.save()
                token = dumps(reset_token)
                link = get_current_site(request).domain + reverse('forgot-password-change') + "?q=" + token
                subject = 'Forgot password'
                message = f"forgot password link <a href='{link}'>click here</a>"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [ 'rathnak010@gmail.com' ]
                send_mail( subject, message, email_from, recipient_list )
        return render(request, 'blog/auth/forgot-password.html', { 'form' : form })
    
class ForgotPasswordChangeView(View):

    def get(self, request, *args, **kwargs):
        reset_token = request.GET.get('q')
        if reset_token is not None:
            try:
                reset_token = loads(reset_token, max_age=3600)
                user = User.objects.get(reset_token=reset_token)
                form  = ForgotPasswordChangeForm()
                return render(request, 'blog/auth/password-change.html', { 'form' : form })
            except:
                pass
        return HttpResponse("reset link expired")
    
    def post(self, request, *args, **kwargs):
        reset_token = request.GET.get('q')
        if reset_token is not None:
            try:
                reset_token = loads(reset_token, max_age=3600)
                user = User.objects.get(reset_token=reset_token)

                form  = ForgotPasswordChangeForm(request.POST)
                if form.is_valid():
                    user.set_password(request.POST.get("password1"))
                    user.reset_token = None
                    user.save()
                    return redirect("login") 
                return render(request, 'blog/auth/password-change.html', { 'form' : form })
            except:
                pass
        return HttpResponse("reset link expired")
    
class ChangePassword(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form  = ForgotPasswordChangeForm()
        return render(request, 'blog/auth/password-change.html', { 'form' : form })
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form  = ForgotPasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password1']
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect('password-change')
        return render(request, 'blog/auth/password-change.html', { 'form' : form })
