from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user.forms import AuthenticationForm


def home_screen_view(request):
    return render(request, 'home.html')


def login_user(request):
    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = AuthenticationForm()

    context['login_form'] = form
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')
