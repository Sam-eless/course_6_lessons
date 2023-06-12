from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

from users.apps import UsersConfig
from django.urls import path

from users.views import ProfileUpdateView, RegisterView, send_verification_email, EmailVerify, MyLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', MyLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verification/', send_verification_email, name='verification'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='invalid_verify.html'), name='invalid_verify'),
    # path('register/genpassword', generate_new_password, name='generate_new_password'),
]
