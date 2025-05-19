from django.urls import path
from app_products.views import ProductsView, MostPurchasedProductsView, MostViewedProductsView, ProductDetailsView, CreateReviewView, terms_and_conditions

urlpatterns=[
    path("",ProductsView.as_view(),name="index"),
    path("products/most-viewed/",MostViewedProductsView.as_view(),name="most-viewed"),
    path("products/best-seller/",MostPurchasedProductsView.as_view(),name="best-seller"),
    path("product-details/<int:pk>/", ProductDetailsView.as_view(), name="product-details"),
    path("product-details/<int:pk>/add-review/", CreateReviewView.as_view(), name="add-review"),
    path("terms/",terms_and_conditions,name="terms-and-conditions"),
]