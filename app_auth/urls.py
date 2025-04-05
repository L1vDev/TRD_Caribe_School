from django.urls import path
from app_auth.views import initial_view, RegisterView, login_view, product_detail, cart,profile

urlpatterns=[
    path("", initial_view,name="index"),
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",login_view,name="login"),
    path("product-details/",product_detail,name="product_detail"),
    path("cart/", cart, name="cart"),
    path("profile/", profile, name="profile"),
    #path("/login/",LoginView,name="login"),
]