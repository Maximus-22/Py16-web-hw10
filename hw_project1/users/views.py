from typing import Any
from django import http
from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
# from django.views.generic.edit import FormView

from .forms import RegisterForm


class RegisterView(View):
    template_name = "users/register.html"
    form_class = RegisterForm

    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect(to="quotes:root")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        # фактично визвали RegisterForm та передали туди запит [POST]
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # всi валiднi даннi з форми потрапляють у спецiальну властивiсть -> <cleaned_data>
            usename = form.cleaned_data["username"]
            # disappear yankies
            messages.success(request, message=f"Вiтаємо {usename}. Ваш аккаунт успiшно створено.")
            return redirect(to="users:login")
        return render(request, self.template_name, context={"form": form})


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/registration/password_reset_form.html"
    email_template_name = "users/registration/password_reset_email.html"
    subject_template_name = "users/registration/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")

    # Перевизначений метод, який викликається при успішній валідації форми
    def form_valid(self, form):
        
        email = form.cleaned_data['email']
        # Перевіряємо, чи є користувач із зазначеним [email] у базі даних
        if not User.objects.filter(email=email).exists():
            # messages.error(self.request, 'This email address is not registered.')            
            self.extra_context = {'error_message': 'Incorrect credentials was entered.'}
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return resolve_url(self.success_url)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/registration/password_reset_confirm.html"