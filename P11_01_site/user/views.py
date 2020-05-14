from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from .forms import LoginForm, NewAccount
from django.template import loader
from django.contrib import messages
from django.contrib import auth
from django.core.mail import EmailMessage
from off.models import Contact
from user.forms import ContactForm


def index(request):
    form = ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['user']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            email_body = """\
                <html>
                  <head></head>
                  <body>
                    <p><strong><span style="text-decoration: underline;">Nom d'utilisateur :</span></strong> %s</p>
                    <p>&nbsp;</p>
                    <p><strong><span style="text-decoration: underline;">Email :</span></strong> %s</p>
                    <p>&nbsp;</p>
                    <p><strong><span style="text-decoration: underline;">Message :</span></strong> %s</p>
                    <p>&nbsp;</p>
                  </body>
                </html>
                """ % (user, email, message)
            email_response = """\
                <html>
                    <head></head>
                    <body>
                        <div class="col-lg-10" style="margin-bottom: auto; margin-top: auto;">
                            <h1 style="text-align: center;">Votre message a bien été pris en compte</h1>
                            <h3 style="text-align: center;">Notre équipe vous repondra dans les plus brefs délais</h3>
                        </div>
                    </body>
                </html>
                """
            email_info = EmailMessage('Mail from contact!', email_body, to=['purbeurre.paris@gmail.com'])
            email_info.content_subtype = "html" # this is the crucial part 
            email_info.send()
            email_info_costumer = EmailMessage('Pure Beurre - Message recu', email_response, to=[email])
            email_info_costumer.content_subtype = "html"
            email_info_costumer.send()
            info = "Message envoyé"
            contact = Contact.objects.create(user=user, email=email, message=message)
            contact.save()
            return render(request, 'off/index.html', {'info': info})
    else:
        return render(request, 'off/index.html', {'form': form})


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
