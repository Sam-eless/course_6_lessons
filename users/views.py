from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, CreateView
from config.settings import EMAIL_HOST_USER
from users.models import User
from users.forms import UserForm, UserRegisterForm, UserAuthenticationForm, CustomSetPasswordForm, \
    CustomPasswordResetForm
from users.utils import send_verify_email


class MyLoginView(LoginView):
    form_class = UserAuthenticationForm


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        return self.request.user

    extra_context = {
        'title': 'Профиль'
    }


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_verify_email(request, user)

        context = {
            'form': form
        }

        return render(request, 'users/login.html', context)


User_data = get_user_model()


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        print(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            login(request, user)
            return redirect('catalog:contacts')
        else:
            return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            print(uid)
            user = User_data.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User_data.DoesNotExist):
            user = None
        return user


# PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')
    template_name = 'users/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
