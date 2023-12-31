from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.forms import CharField, EmailField, EmailInput, TextInput, PasswordInput
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    username = CharField(max_length=24, min_length=5, required=True, widget=TextInput(attrs={"class": "form-control"}))
    email = EmailField(max_length=48, required=True, widget=EmailInput(attrs={"class": "form-control"}))
    password1 = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))
    password2 = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    # Django очікує, що метод для валідації поля називатиметься clean_<field_name>
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This login for user is already in use.')
        return username


class LoginForm(AuthenticationForm):
    username = CharField(max_length=24, min_length=5, required=True, widget=TextInput(attrs={"class": "form-control"}))
    password = CharField(required=True, widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "password")


class PatrolSetPasswordForm(SetPasswordForm):
    
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']