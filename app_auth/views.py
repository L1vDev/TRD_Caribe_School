from django.shortcuts import render
import json
import random
from functools import lru_cache

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from app_auth.forms import RegisterForm, LoginForm
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import login, authenticate, logout
from app_auth.utils import generate_token,verify_token, send_verification_email
from django.urls import reverse
from django.shortcuts import redirect
from app_auth.models import User

def initial_view(request):
    return render(request,"index.html")

def register_view(request):
    return render(request,"auth/register.html")

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

def verify_email_view(request, token):
    payload, is_valid = verify_token(token)
    if is_valid:
        print("is_valid")
        user_email = payload.get('user_email')
        user=User.objects.get(email=user_email) 
        if user is None:
            return render(request, 'auth/email_verification_failed.html')
        print(f"user:{user.email}")
        user.is_email_verified = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'auth/email_verification_failed.html')
    
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
        except Exception as e:
            print(str(e))
        return render(request, self.template_name,{'error':'Credenciales Inválidas'})

def logout_view(request):
    logout(request)
    return redirect('login')

def product_detail(request):
    return render(request,"store/products.html")

def cart(request):
    return render(request,"store/cart.html")

def profile(request):
    return render(request,"auth/profile.html")

def best_seller(request):
    return render(request,"store/best_seller.html")

def most_viewed(request):
    return render(request,"store/most_viewed.html")

def contact(request):
    return render(request,"store/contact.html")

def invoice_list(request):
    return render(request,"store/invoice.html")

def terms_and_conditions(request):
    return render(request,"store/terms.html")

def favorites(request):
    return render(request,"store/favorites.html")

def dashboard_callback(request, context):
    context.update(random_data())
    return context

@lru_cache
def random_data():
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    performance_negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]

    return {
        "navigation": [
            {"title": _("Dashboard"), "link": "/", "active": True},
            {"title": _("Analytics"), "link": "#"},
            {"title": _("Settings"), "link": "#"},
        ],
        "filters": [
            {"title": _("All"), "link": "#", "active": True},
            {
                "title": _("New"),
                "link": "#",
            },
        ],
        "kpi": [
            {
                "title": "Product A Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [{"data": average, "borderColor": "#9333ea"}],
                    }
                ),
            },
            {
                "title": "Product B Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
            },
            {
                "title": "Product C Performance",
                "metric": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">+{intcomma(f"{random.uniform(1, 9):.02f}")}%</strong>&nbsp;progress from last week'
                ),
            },
        ],
        "progress": [
            {
                "title": "🦆 Social marketing e-book",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🦍 Freelancing tasks",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🐋 Development coaching",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🦑 Product consulting",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🐨 Other income",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🐶 Course sales",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🐻‍❄️ Ads revenue",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🦩 Customer Retention Rate",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🦊 Marketing ROI",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
            {
                "title": "🦁 Affiliate partnerships",
                "description": f"${intcomma(f'{random.uniform(1000, 9999):.02f}')}",
                "value": random.randint(10, 90),
            },
        ],
        "chart": json.dumps(
            {
                "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                "datasets": [
                    {
                        "label": "Example 1",
                        "type": "line",
                        "data": average,
                        "borderColor": "var(--color-primary-500)",
                    },
                    {
                        "label": "Example 2",
                        "data": positive,
                        "backgroundColor": "var(--color-primary-700)",
                    },
                    {
                        "label": "Example 3",
                        "data": negative,
                        "backgroundColor": "var(--color-primary-300)",
                    },
                ],
            }
        ),
        "performance": [
            {
                "title": _("Last week revenue"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_positive,
                                "borderColor": "var(--color-primary-700)",
                            }
                        ],
                    }
                ),
            },
            {
                "title": _("Last week expenses"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_negative,
                                "borderColor": "var(--color-primary-300)",
                            }
                        ],
                    }
                ),
            },
        ],
    }