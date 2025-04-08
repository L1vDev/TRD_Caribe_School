from django.urls import path
from app_auth.views import initial_view, RegisterView, login_view, product_detail, cart,profile, best_seller, most_viewed, contact, invoice_list

urlpatterns=[
    path("", initial_view,name="index"),
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",login_view,name="login"),
    path("product-details/",product_detail,name="product_detail"),
    path("cart/", cart, name="cart"),
    path("profile/", profile, name="profile"),
    path("products/most-viewed/",most_viewed,name="most_viewed"),
    path("products/best-seller/",best_seller,name="best_seller"),
    path("contact/",contact,name="contact"),
    path("invoice/",invoice_list,name="invoice_list"),
    #path("/login/",LoginView,name="login"),
]