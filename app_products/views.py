from django.shortcuts import render
from app_products.models import Products, Reviews
from django.views.generic import CreateView, ListView
from django.views import View
from django.db.models import F, Avg, Count, Value, ExpressionWrapper, DecimalField, Q, Sum
from django.db.models.functions import Coalesce, Round
from django.utils import timezone
from django.db.models.functions import Now

class ProductsView(ListView):
    """
    AÑADIR PAGINACION A LOS PRODUCTOS
    """

    queryset = Products.objects.filter(available=True).annotate(
        stars=Coalesce(Avg('reviews__rating'), Value(float(0))),
        discount_price=Round(
            ExpressionWrapper(
                F('price') * (1 - F('discount') / 100),
                output_field=DecimalField()
            ), 2
        ),
        is_new=ExpressionWrapper(
            Q(created_at__gte=Now() - timezone.timedelta(days=3)),
            output_field=DecimalField()
        )
    ).all()
    template_name = "index.html"
    context_object_name = "products"

class MostViewedProductsView(ListView):
    queryset = Products.objects.filter(available=True).annotate(
        stars=Coalesce(Avg('reviews__rating'), Value(float(0))),
        discount_price=Round(
            ExpressionWrapper(
                F('price') * (1 - F('discount') / 100),
                output_field=DecimalField()
            ), 2
        ),
        is_new=ExpressionWrapper(
            Q(created_at__gte=Now() - timezone.timedelta(days=3)),
            output_field=DecimalField()
        )
    ).order_by("-views").all()[:10]
    template_name="store/most_viewed.html"
    context_object_name="products"

class MostPurchasedProductsView(ListView):
    queryset = Products.objects.filter(available=True).annotate(
        stars=Coalesce(Avg('reviews__rating'), Value(float(0))),
        discount_price=Round(
            ExpressionWrapper(
                F('price') * (1 - F('discount') / 100),
                output_field=DecimalField()
            ), 2
        ),
        is_new=ExpressionWrapper(
            Q(created_at__gte=Now() - timezone.timedelta(days=3)),
            output_field=DecimalField()
        )
    ).order_by("-purchases").all()[:10]
    template_name="store/best_seller.html"
    context_object_name="products"

class ProductDetailsView(ListView):
    model=Products
    template_name = "store/product_details.html"

    def get_context_data(self,**kwargs):
        """
        AJUSTAR IMAGENES EN EL INDICE
        AÑADIR PAGINACION A REVIEW Y RELATED PRODUCTS
        """
        context=super(ProductDetailsView, self).get_context_data(**kwargs)
        product= Products.objects.filter(id=self.kwargs.get('pk'), available=True).annotate(
            stars=Coalesce(Avg('reviews__rating'), Value(float(0))),
            discount_price=Round(
                ExpressionWrapper(
                    F('price') * (1 - F('discount') / 100),
                    output_field=DecimalField()
                ), 2
            ),
            is_new=ExpressionWrapper(
                Q(created_at__gte=Now() - timezone.timedelta(days=3)),
                output_field=DecimalField()
            )
        ).first()
        product.views=product.views+1
        product.save()
        reviews=Reviews.objects.filter(product=product).all()
        stars_count_qs = reviews.values('rating').annotate(count=Count('id'))
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
        ).annotate(
            stars=Coalesce(Avg('reviews__rating'), Value(float(0))),
            discount_price=Round(
                ExpressionWrapper(
                    F('price') * (1 - F('discount') / 100),
                    output_field=DecimalField()
                ), 2
            ),
        ).exclude(id=product.id).distinct()[:4]

        context["stars_percent"] = stars_percent
        context["related_products"] = related_products
        context["product"]=product
        context["reviews"]=reviews
        return context
