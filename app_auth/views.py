from django.shortcuts import render
import json
import random
from functools import lru_cache

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from app_auth.forms import RegisterForm, LoginForm, ResetPasswordForm
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from app_auth.utils import generate_token,verify_token, send_verification_email, send_reset_password_email
from django.urls import reverse
from django.shortcuts import redirect
from app_auth.models import User
from app_store.models import Cart

class RegisterView(CreateView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('verify-email-alert')

    def form_valid(self, form):
        user = form.save()
        token=generate_token(user)
        domain = self.request.get_host()  
        scheme = 'https' if self.request.is_secure() else 'http' 
        verification_url = f"{scheme}://{domain}{reverse('verify-email', kwargs={'token': token})}"
        send_verification_email(user, verification_url)
        return super().form_valid(form)
    
def verify_email_alert(request):
    return render(request, 'auth/verify_email.html')

def verify_email_failed(request):
    return render(request, 'auth/email_verification_failed.html')

def verify_email_view(request, token):
    payload, is_valid = verify_token(token)
    if is_valid:
        print("is_valid")
        user_email = payload.get('user_email')
        user=User.objects.get(email=user_email) 
        if user is None:
            return redirect("verify-email-failed")
        print(f"user:{user.email}")
        user.is_email_verified = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return redirect("verify-email-failed")
    
class LoginView(View):
    template_name="auth/login.html"
    form_class=LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self,request,*args,**kwargs):
        try:
            form=self.form_class(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                try:
                    user=User.objects.get(email=email)
                    user=authenticate(request, username=user.email,password=password)
                    if user is not None:
                        if not user.is_email_verified:
                            token=generate_token(user)
                            domain = request.get_host()  
                            scheme = 'https' if request.is_secure() else 'http' 
                            verification_url = f"{scheme}://{domain}{reverse('verify-email', kwargs={'token': token})}"
                            send_verification_email(user, verification_url)
                            return render(request, self.template_name,{'error':'Email por verificar. Revise su bandeja de entrada.'})
                        login(request,user)
                        return redirect('index')
                except User.DoesNotExist:
                    print("user does not exist")
                    return render(request, self.template_name,{'error':'Credenciales Inválidas'})
            elif request.POST.get('forgot_password_email'):
                email=request.POST.get('forgot_password_email')
                user=User.objects.filter(email=email).first()
                if not user:
                    return render(request, self.template_name,{'error':'No existe una cuenta con este correo electrónico.'})
                token=generate_token(user)
                domain = request.get_host()  
                scheme = 'https' if request.is_secure() else 'http' 
                verification_url = f"{scheme}://{domain}{reverse('reset-password', kwargs={'token': token})}"
                send_reset_password_email(user, verification_url)
                return redirect('reset-password-alert')
        except Exception as e:
            print(str(e))
        return render(request, self.template_name,{'error':'Credenciales Inválidas'})

def logout_view(request):
    logout(request)
    return redirect('login')

def reset_password_email_alert(request):
    return render(request, 'auth/reset_password_email.html')

def reset_password_email_failed(request):
    return render(request, 'auth/reset_password_failed.html')

class ResetPasswordView(View):
    template_name='auth/reset_password_form.html'
    form_class=ResetPasswordForm

    def get(self, request, token, *args, **kwargs):
        payload, is_valid=verify_token(token)
        if is_valid:
            user=User.objects.filter(email=payload["user_email"]).first()
            if not user:
                return redirect('reset-password-failed')
            return render(request,self.template_name,{"token":token})
        else:
            return redirect('reset-password-failed')
        
    
    def post(self, request, token, *args, **kwargs):
        try:
            payload, is_valid=verify_token(token)
            if is_valid:
                email=payload["user_email"]
                form=self.form_class(request.POST)
                if form.is_valid():
                    new_password=form.cleaned_data['new_password']
                    try:
                        user=User.objects.get(email=email)
                        if user is not None:
                            user.set_password(new_password)
                            user.save()
                        login(request,user)
                        return redirect('index')
                    except User.DoesNotExist:
                        print("user does not exist")
                        return render(request, self.template_name,{'error':'Ha ocurrido un error al recuperar la contraseña'})
        except Exception as e:
            print(str(e))
        return render(request, self.template_name,{'error':'Ha ocurrido un error al recuperar la contraseña'})

class ProfileView(LoginRequiredMixin, View):
    template_name="auth/profile.html"

    def get_context_data(self, request):
        user=request.user
        cart, created=Cart.objects.get_or_create(user=user)
        cart_count=cart.products.count()
        context={
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "phone_number":user.phone_number,
            "profile_picture":user.profile_picture.url if user.profile_picture else None,
            "cart_count":cart_count,
        }
        return context

    def get(self, request, *args, **kwargs):
        context=self.get_context_data(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user=request.user
        error=""
        if "delete_account" in request.POST:
            user.delete()
            logout(request)
            return redirect("index")
        elif "change_password" in request.POST:
            old_password=request.POST.get("current_password")
            new_password=request.POST.get("new_password")
            confirm_password=request.POST.get("confirm_password")
            if user.check_password(old_password):
                if new_password==confirm_password:
                    user.set_password(new_password)
                    user.save()
                    login(request,user)
                else:
                    error="Las contraseñas no coinciden."
            else:
                error="Su contraseña actual es incorrecta."
        elif "remove_picture" in request.POST:
            user.profile_picture=None
        else:
            user.first_name=request.POST.get("first_name")
            user.last_name=request.POST.get("last_name")
            user.phone_number=request.POST.get("phone_number")
            if "profile_picture" in request.FILES:
                profile_picture = request.FILES["profile_picture"]
                user.profile_picture.save(profile_picture.name, profile_picture, save=False)
        try:
            user.save()
        except Exception as e:
            error="No se pudo guardar los cambios, revise la información introducida."
        context={
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email,
            "phone_number":user.phone_number,
            "profile_picture":user.profile_picture.url if user.profile_picture else None,
        }
        if error:
            context["errors"]=error
        else:
            context["success"]="Perfil actualizado correctamente"
        return render(request, self.template_name, context)

