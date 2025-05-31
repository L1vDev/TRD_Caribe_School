from typing import Any
from django.shortcuts import render
from app_products.models import Products, Reviews, Category
from django.views.generic import CreateView, ListView
from django.views import View
from django.db.models import F, Avg, Count, Value, ExpressionWrapper, DecimalField, Q, Sum
from django.db.models.functions import Coalesce, Round
from django.utils import timezone
from django.db.models.functions import Now
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from app_store.models import Cart, CartItem
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re
import unicodedata
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("spanish")

def stem_text(text):
    normalized_term = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()
    words = normalized_term.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words

class ProductsView(ListView):
    """
    AÑADIR PAGINACION A LOS PRODUCTOS
    """
    template_name = "index.html"
    paginate_by = 16

    def get_queryset(self):
        queryset = Products.objects.filter(available=True).order_by("id")
        search = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        if search:
            stemmed_words = stem_text(search)
            query = Q()
            for word in stemmed_words:
                query &= Q(canon_name__icontains=word)
            queryset = queryset.filter(query)
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            context["cart_count"] = cart.products.count()
        # Mantener valores de búsqueda y categoría seleccionados
        context["search"] = self.request.GET.get('search', '')
        context["category"] = self.request.GET.get('category', '')
        # Si necesitas pasar todas las categorías al template:
        context["categories"] = Category.objects.all()
        context["show_filters"] = True
        return context

class MostViewedProductsView(ListView):
    template_name = "store/most_viewed.html"
    paginate_by = 16

    def get_queryset(self):
        queryset = Products.objects.filter(available=True).order_by("-views")
        search = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        if search:
            stemmed_words = stem_text(search)
            query = Q()
            for word in stemmed_words:
                query &= Q(canon_name__icontains=word)
            queryset = queryset.filter(query)
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            context["cart_count"] = cart.products.count()
        context["search"] = self.request.GET.get('search', '')
        context["category"] = self.request.GET.get('category', '')
        context["categories"] = Category.objects.all()
        context["show_filters"] = True
        return context

class MostPurchasedProductsView(ListView):
    template_name = "store/best_seller.html"
    paginate_by = 16

    def get_queryset(self):
        queryset = Products.objects.filter(available=True).order_by("-purchases")
        search = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        if search:
            stemmed_words = stem_text(search)
            query = Q()
            for word in stemmed_words:
                query &= Q(canon_name__icontains=word)
            queryset = queryset.filter(query)
        if category:
            queryset = queryset.filter(category__id=category)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            context["cart_count"] = cart.products.count()
        context["search"] = self.request.GET.get('search', '')
        context["category"] = self.request.GET.get('category', '')
        context["categories"] = Category.objects.all()
        context["show_filters"] = True
        return context

class ProductDetailsView(ListView):
    model=Products
    template_name = "store/product_details.html"

    def get_context_data(self,**kwargs):
        """
        AJUSTAR IMAGENES EN EL INDICE
        AÑADIR PAGINACION A REVIEW Y RELATED PRODUCTS
        """
        product= get_object_or_404(Products,id=self.kwargs.get('pk'), available=True)
        context=super(ProductDetailsView, self).get_context_data(**kwargs)
        user=self.request.user
        if user.is_authenticated:
            cart, created=Cart.objects.get_or_create(user=user)
            context["cart_count"]=cart.products.count()
        product.views=product.views+1
        product.save()
        reviews_qs=Reviews.objects.filter(product=product).all()

        page = self.request.GET.get('page')
        paginator = Paginator(reviews_qs, 10)
        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)

        stars_count_qs = reviews_qs.values('rating').annotate(count=Count('id'))
        total_reviews = stars_count_qs.aggregate(total=Coalesce(Sum('count'), Value(0)))['total'] or 1

        stars_count = {str(i): 0 for i in range(1, 6)}
        for item in stars_count_qs:
            stars_count[str(item['rating'])] = item['count']

        stars_percent = {}
        for i in range(5, 0, -1):
            percent = round((stars_count[str(i)] / total_reviews) * 100, 2)
            stars_percent[str(i)] = {
            "percent": percent,
            "percent_int": int(percent)
            }

        related_products = Products.objects.filter(
            available=True,
            category__in=product.category.all()
        ).exclude(id=product.id).distinct()

        context["stars_percent"] = stars_percent
        context["related_products"] = related_products
        context["product"]=product
        context["reviews"]=reviews
        context["paginator"] = paginator
        item=CartItem.objects.filter(cart=cart,product=product)
        context["product_quantity"]=(item.first().quantity if item.exists() else 1)
        return context

class CreateReviewView(LoginRequiredMixin,View):

    def post(self,request,pk,*args,**kwargs):
        if request.method=="POST":
            product=Products.objects.get(pk=pk)
            user=request.user
            comment=request.POST.get("comment", "")
            rating=request.POST.get("rating",5)
            Reviews.objects.create(
                product=product,
                user=user,
                comment=comment,
                rating=rating,
            )
            return redirect('product-details',pk=pk)

def terms_and_conditions(request):
    context={}
    user=request.user
    if user.is_authenticated:
        cart,created=Cart.objects.get_or_create(user=user)
        context["cart_count"]=cart.products.count()
    return render(request,"store/terms.html",context)