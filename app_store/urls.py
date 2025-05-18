from django.urls import path
from app_store.views import CartView, AddCartView, UpdateCartView, DeleteCartView, ListInvoicesView

urlpatterns=[
    path("cart/",CartView.as_view(),name="cart"),
    path("cart/<int:pk>/add/",AddCartView.as_view(),name="add-to-cart"),
    path("cart/update/",UpdateCartView.as_view(), name="update-cart"),
    path("cart/delete/",DeleteCartView.as_view(), name="delete-cart"),
    path("order/list/", ListInvoicesView.as_view(), name="order-list"),
    #path("order/create/",CreateInvoiceView.as_view(),name="order-create"),
]