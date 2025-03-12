from django.urls import path
from app_auth.views import initial_view

urlpatterns=[
    path("", initial_view,name="index")
    #path("/register/",RegisterView,name="register"),
    #path("/login/",LoginView,name="login"),
]