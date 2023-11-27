from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


class RegisterView(View):
    template_name = "users/register.html"
    form_class = RegisterForm

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
