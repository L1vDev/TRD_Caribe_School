from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactRequest
from app_store.models import Cart

class ContactRequestView(View):
    template_name = 'store/contact.html'

    def get_context_data(self, request):
        context={}
        user=request.user
        if user.is_authenticated:
            cart, created=Cart.objects.get_or_create(user=user)
            context["cart_count"]=cart.products.count()
        return context

    def get(self, request):
        context=self.get_context_data(request)
        return render(request, self.template_name,context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        contact = ContactRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            message=message
        )
        return redirect('index') 
