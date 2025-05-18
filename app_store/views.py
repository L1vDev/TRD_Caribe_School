from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from app_store.models import Cart, CartItem, Invoices, InvoiceProducts
from django.views import View
from django.views.generic import ListView
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Round
from app_products.models import Products
from app_config.models import Province, Municipality
import json
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
import os
from django.shortcuts import get_object_or_404
        
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
    
    def post(self, request, *args, **kwargs):
        user=request.user
        context=self.get_context_data()
        cart=Cart.objects.filter(user=user).first()
        cart_items=CartItem.objects.filter(cart=cart).all()
        over_stock=False
        low_stock=False
        for item in cart_items:
            if item.product.stock==0:
                low_stock=True
            elif item.quantity>item.product.stock:
                over_stock=True
        
        if low_stock:
            context["error"]="Algunos productos se han agotado. Retírelos del carrito para poder comprar."
            return render(request, self.template_name,context)
        elif over_stock:
            context["error"]="Algunos productos no tienen stock suficiente. Modifique las cantidades."
            return render(request, self.template_name,context)

        province_id=request.POST.get("province")
        municipality_id=request.POST.get("municipality")
        province=Province.objects.get(pk=province_id)
        municipality=Municipality.objects.get(pk=municipality_id)
        
        try:
            with transaction.atomic():
                invoice = Invoices.objects.create(
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    phone_number=request.POST.get("phone_number", user.phone_number),
                    province=province.name,
                    municipality=municipality.name,
                    address=request.POST.get("address", ""),
                    delivery_details=request.POST.get("delivery_details", ""),
                    delivery_price=municipality.price,
                )

                for item in cart_items:
                    item.product.stock = item.product.stock - item.quantity
                    item.product.save()
                    InvoiceProducts.objects.create(
                    invoice=invoice,
                    product_id=item.product.id,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    product_discount=item.product.discount,
                    quantity=item.quantity
                    )
                invoice.generate_pdf()
        except Exception as e:
            print(str(e))
            context["error"] = "Ha ocurrido un error al realizar la compra. Por favor, intente de nuevo."
            return render(request, self.template_name, context)
        
        cart.delete()
        Cart.objects.create(user=user)
        return redirect("order-list")
    
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

class ListInvoicesView(LoginRequiredMixin, ListView):
    template_name = "store/invoice.html"

    def get_queryset(self):
        user=self.request.user
        invoices=Invoices.objects.filter(email=user.email).all()
        return invoices
    
    def get_context_data(self, **kwargs):
        context=super(ListInvoicesView, self).get_context_data(**kwargs)
        invoices=self.get_queryset()
        context["invoices"]=invoices
        return context

@login_required
def download_invoice_pdf(request, pk):
    user = request.user
    try:
        if user.is_superuser:
            invoice = get_object_or_404(Invoices, pk=pk)
        else:
            invoice = get_object_or_404(Invoices, pk=pk, email=user.email)
        file_path = invoice.invoice_file.path

        if not os.path.exists(file_path):
            return HttpResponse("Archivo no encontrado.", status=404)
        pdf_file = open(file_path, 'rb')
        response = FileResponse(pdf_file, as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(invoice.invoice_file.name)}"'
        return response

    except Invoices.DoesNotExist:
        return HttpResponse("Factura no encontrada.", status=404)
    except Exception:
        return HttpResponse("No autorizado o error interno.", status=401)
