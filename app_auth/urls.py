from django.urls import path
from app_auth.views import initial_view, RegisterView,verify_email_alert,verify_email_view, LoginView,logout_view, product_detail, cart,profile, best_seller, most_viewed, contact, invoice_list, terms_and_conditions, favorites

urlpatterns=[
    path("", initial_view,name="index"),
    path("register/",RegisterView.as_view(),name="register"),
    path("verify-email/",verify_email_alert,name="verify-email-alert"),
    path("verify-email/<str:token>/",verify_email_view,name="verify-email"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",logout_view,name="logout"),
    path("product-details/",product_detail,name="product-details"),
    path("cart/", cart, name="cart"),
    path("profile/", profile, name="profile"),
    path("products/most-viewed/",most_viewed,name="most-viewed"),
    path("products/best-seller/",best_seller,name="best-seller"),
    path("contact/",contact,name="contact"),
    path("invoice/",invoice_list,name="invoice-list"),
    path("terms/",terms_and_conditions,name="terms-and-conditions"),
    path("favorites/",favorites,name="favorites"),
    #path("/login/",LoginView,name="login"),
]