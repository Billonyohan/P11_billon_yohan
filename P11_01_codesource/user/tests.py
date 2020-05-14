from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import LoginForm, NewAccount


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='johnpassword', email='lennon@thebeatles.com')
    """test page account"""
    def test_account(self):
        self.client.login(username='john', password='johnpassword')
        user = User.objects.get(username="john")
        self.client.force_login(self.user)
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
    """test new account page"""
    def test_new_account(self):
        john = 'john'
        johnpassword = "johnpassword"
        email = 'lennon@thebeatles.com'
        form = {'username': john,
                'email': email,
                'password1': johnpassword,
                'password2': johnpassword,
                }
        response = self.client.post(reverse('new_account'), form)
        self.assertEqual(response.status_code, 200)
    """test loginView """
    def test_loginView(self):
        user = User.objects.get(username="john")
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 200)
    """test if user is authenticated"""
    def test_loginView_connected(self):
        self.client.login(username='john', password='johnpassword')
        user = User.objects.get(username="john")
        self.client.force_login(self.user)
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 302)


class LogoutTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', password='johnpassword', email='lennon@thebeatles.com')
        self.client.login(username='john', password='johnpassword')
    """return the logout page"""
    def test_logoutView(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

class ContactTestCase(TestCase):
    def setUp(self):
        username = "marc"
        email = "aflf@gmail.com"
        message = "ok"
        self.form = {'username': username,
                    'email': email,
                    'message': message,
                    }

    def test_index(self):
        response = self.client.post(reverse('index'), self.form)
        self.assertEqual(response.status_code, 200)