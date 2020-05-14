from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
"""Forms for create new account"""


class NewAccount(UserCreationForm):

    username = forms.CharField(max_length=30, required=True,
                             label=("Nom d’utilisateur"),
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(max_length=150, required=True,
                             label=("Adresse électronique"),
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(max_length=30,
                                label=("Mot de passe"),
                                strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(max_length=30,
                                label=("Confirmation du mot de passe"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                strip=False,)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewAccount, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """form for user's login"""
    username = UsernameField(
            widget=forms.TextInput(attrs={
                'autofocus': True,
                'class': 'form-control'})
    )
    password = forms.CharField(
            label=("Password"),
            strip=False,
            widget=forms.PasswordInput(attrs={
                'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class ContactForm(forms.Form):
    user = forms.CharField(label="Nom d'utilisateur", required=False)
    email = forms.EmailField(required=True, label="Email")
    message = forms.CharField(widget=forms.Textarea, required=True)
    
