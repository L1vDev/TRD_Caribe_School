from django.urls import path
from app_auth.views import RegisterView,verify_email_alert,verify_email_failed,verify_email_view, LoginView,logout_view,reset_password_email_alert,reset_password_email_failed, ResetPasswordView,ProfileView

urlpatterns=[
    path("register/",RegisterView.as_view(),name="register"),
    path("verify-email/",verify_email_alert,name="verify-email-alert"),
    path("verify-email-failed/",verify_email_failed,name="verify-email-failed"),
    path("verify-email/<str:token>/",verify_email_view,name="verify-email"),
    path("login/",LoginView.as_view(),name="login"),
    path("logout/",logout_view,name="logout"),
    path("reset-password/",reset_password_email_alert,name="reset-password-alert"),
    path("reset-password-failed/",reset_password_email_failed,name="reset-password-failed"),
    path("reset-password/<str:token>/",ResetPasswordView.as_view(),name="reset-password"),
    path("profile/", ProfileView.as_view(), name="profile"), #add js validation
    
]