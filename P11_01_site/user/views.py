from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from .forms import LoginForm, NewAccount
from django.template import loader
from django.contrib import messages
from django.contrib import auth

def index(request):
    return render(request, 'off/index.html')


@login_required
def account(request):
    """returns account page"""
    return render(request, 'off/account.html')


def new_account(request):
    """returns new_account page"""
    if request.method == 'POST':
        form = NewAccount(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            return redirect('login')
    else:
        form = NewAccount()
    return render(request, 'off/new_account.html', {'form': form})


def loginView(request):
    """return login page and test if user data connexion is valid"""
    if request.user.is_authenticated:
        return redirect('account')
    else:
        login = LoginForm(request.POST)
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('account')
            else:
                messages.error(request, '/!\\ Erreur sur votre nom d’utilisateur ou votre mot de passe /!\\')
        log = LoginForm()
        return render(request, 'off/login.html', {
            'form': log,
            })


@login_required
def logoutView(request):
    """logout account returns home page"""
    logout(request)
    return redirect('index')
