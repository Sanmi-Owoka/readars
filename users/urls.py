from django.urls import path
from .views.register_user_view import RegisterView
from .views.login_view import LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register_user"),
    path("login/", LoginView.as_view(), name="login_user")
]