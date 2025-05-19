from django.urls import path
from app_config.views import ContactRequestView

urlpatterns=[
    path("contact/",ContactRequestView.as_view(),name="contact")
]