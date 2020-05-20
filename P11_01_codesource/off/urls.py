from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from off import views

urlpatterns = [url(r'^result$', views.result_search, name='result_search'),
               url(r'^aliment/description$', views.food_details, name='description'),
               url(r'^aliment/substitut$', views.substitute, name="substitute"),
               url(r'^mentions_légales$', views.legal, name="legal"),
               url(r'^substituts/sauvegardé$', views.saved_substitute, name="saved_substitute"),
               url(r'^aliment/substituts/sauvegardé$', views.substitute_saved, name="substitute_saved"),
               ]
