from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from app_store.models import Cart, CartItem
from django.views import View
        
class CartView(LoginRequiredMixin,View):
    template_name="store/cart.html"

    def get_context_data(self,**kwargs):
        pass

    def get(self,request,*args,**kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        print("aguacate")
