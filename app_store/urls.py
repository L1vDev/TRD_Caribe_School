from django.urls import path
from app_store.views import CartView

urlpatterns=[
    path("cart/",CartView.as_view(),name="cart"),
]