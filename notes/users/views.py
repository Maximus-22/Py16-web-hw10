from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm, ProfileForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='noteapp:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='noteapp:main')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='noteapp:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # В Django [messages] - это механизм, который позволяет передавать сообщения от одной части кода к другой через запросы.
            # Он часто используется для отображения уведомлений или ошибок на следующей странице, когда запрос перенаправляется.
            # Чтобы использовать эти сообщения в шаблоне, нужно включить соответствующий тег в соответствующем шаблоне.
            # В нашем случае - в шаблоне users/login.html есть вставка:
            # {% if messages %} ... {% endif %}
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='noteapp:main')

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='noteapp:main')


# @login_required
# def profile(request):
#     return render(request, 'users/profile.html')

@login_required
def profile(request):
    # Коли форма відправлена, потрібно передати дані запиту [request.POST] у форму ProfileForm. Але для форми профілю
    # є дані у вигляді файлу зображення, які надійшли разом із запитом. Ці дані файлу розміщені в об'єкті [request.FILES],
    # тому вони також потрібнi.
    # Користувальницька форма очікує на екземпляр користувача, оскільки вона працює з моделлю користувача User, тому для
    # форми профілю потрiбно передати в екземпляр моделі профілю параметр <instance = request.user.profile>.
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'profile_form': profile_form})