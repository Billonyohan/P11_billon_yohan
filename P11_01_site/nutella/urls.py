"""nutella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from off import views
from user import views

urlpatterns = [
            url(r'^$', views.index, name="index"),
            url(r'^off/', include('off.urls')),
            url(r'^admin/', admin.site.urls),
            url(r'^login$', views.loginView, name='login'),
            url(r'^nouveau$', views.new_account, name='new_account'),
            url(r'^compte$', views.account, name='account'),
            url(r'^logout$', views.logoutView, name='logout')
            ]
