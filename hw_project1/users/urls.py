from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm, PatrolSetPasswordForm


app_name = 'users'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name = 'signup'),
    path('login/', auth_views.LoginView.as_view(template_name = "users/login.html", form_class = LoginForm,
                                                redirect_authenticated_user = True), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = "users/logout.html"), name = 'logout'),
    path('password_reset/',
         views.PatrolPasswordResetView.as_view(template_name = "users/registration/password_reset_form.html"),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name = "users/registration/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.ChangeUserPasswordView.as_view(template_name = "users/registration/password_reset_confirm.html", 
         form_class = PatrolSetPasswordForm), name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name = "users/registration/password_reset_complete.html"),
         name='password_reset_complete'),
]