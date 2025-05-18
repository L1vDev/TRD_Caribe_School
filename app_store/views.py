from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from app_store.models import Cart, CartItem
from django.views import View
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Round
from app_products.models import Products
from app_config.models import Province, Municipality
import json
        
class CartView(LoginRequiredMixin,View):
    template_name="store/cart.html"

    def get_context_data(self,**kwargs):
        context={}
        user=self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart).all()
        provinces=Province.objects.all()
        municipalitites_by_province={}
        for province in provinces:
            municipalitites_by_province[province.id]=[
                {"id":m.id, "name":m.name, "price":float(m.price)} for m in province.municipalities.all()
            ]
        context['municipalities']=json.dumps(municipalitites_by_province)
        context["provinces"]=provinces
        context["cart_items"]=cart_items
        context["subtotal"]=cart.get_subtotal()
        return context 

    def get(self,request,*args,**kwargs):
        context=self.get_context_data()
        return render(request, self.template_name,context)
    
class AddCartView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        product=Products.objects.filter(available=True, pk=pk).first()
        user=request.user
        cart, created=Cart.objects.get_or_create(user=user)
        quantity=int(request.POST.get("quantity",0))
        quantity=quantity if quantity<product.stock else product.stock
        cart_item,created=CartItem.objects.get_or_create(
            product=product,
            cart=cart,
        )
        cart_item.quantity=quantity
        cart_item.save()

        return redirect("cart")

class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id=request.POST.get("product_id")
        quantity=request.POST.get("quantity")
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item = CartItem.objects.filter(cart=cart, product__id=product_id).first()
        if cart_item:
            cart_item.quantity=quantity
            cart_item.save()
        return redirect("cart")
    
class DeleteCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item_id=request.POST.get("cart_item_id")
        cart_item = CartItem.objects.filter(id=cart_item_id).first()
        if cart_item:
            cart_item.delete()
        return redirect("cart")