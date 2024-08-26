from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

app_name = "accounts"
from django.views.generic import RedirectView

urlpatterns = [
    path("signup/", views.FtSignupView.as_view(), name="signup"),
    path("signup-two-fa/", views.SignupTwoFAView.as_view(), name="signup-two-fa"),
    path("login/", views.FtLoginView.as_view(), name="login"),
    path("login-two-fa/", views.LoginTwoFAView.as_view(), name="login-two-fa"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", RedirectView.as_view(url="/accounts/login/")),
]
