from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.template import loader
from .models import Food, Substitute
from django.contrib import messages
from django.http import HttpResponse


def result_search(request):
    """returns result search page with food"""
    query = request.GET.get('query')
    foods = Food.objects.filter(food__icontains=query)
    paginator = Paginator(foods, 6)
    page = request.GET.get('page')
    paginator_food = paginator.get_page(page)
    if foods.count() <= 0:
        return render(request, 'off/result_search.html', {
            'nofoods': "Aucun aliment trouvé !",
            })
    else:
        return render(request, 'off/result_search.html', {
            "foods": paginator_food,
            "foods2": query
            })


def food_details(request):
    """returns food page with details"""
    details = request.GET.get('details')
    foods_details = Food.objects.filter(food__icontains=details)[:1]
    return render(request, 'off/food_details.html', {
        'foods': foods_details,
        })


def substitute(request):
    """return substitute page"""
    foods_substitute = request.GET.get('foods_subtitute')
    foods_substitute2 = request.GET.get('saved_substitute2')
    subtitute = Food.objects.filter(food__icontains=foods_substitute).order_by('nutriscore').exclude(food__contains=foods_substitute)
    paginator = Paginator(subtitute, 6)
    page = request.GET.get('page')
    paginator_substitute = paginator.get_page(page)
    if subtitute.count() >= 1:
        return render(request, 'off/substitute.html', {
            'foods_substitute': paginator_substitute,
            'foods_substitute2': foods_substitute2,
            'substitute': foods_substitute
            })
    else:
        substitute_food = foods_substitute.split()
        substitute2 = Food.objects.filter(food__contains=substitute_food[0]).order_by('nutriscore').exclude(food__contains=foods_substitute)
        paginator = Paginator(substitute2, 6)
        page = request.GET.get('page')
        paginator_substitute = paginator.get_page(page)
        if substitute2.count() >= 1:
            return render(request, 'off/substitute.html', {
                'foods_substitute': paginator_substitute,
                'foods_substitute2': foods_substitute2,
                'substitute': foods_substitute
                })
        else:
            return render(request, 'off/substitute.html', {
                'nosubstitute': "Aucun substitut trouvé !",
                })


@login_required
def saved_substitute(request):
    """get food and subtitutes saved and return them to substitute_saved views"""
    substitute_food = request.GET.get('saved_substitute')
    substitute_food2 = request.GET.get('saved_substitute2')
    substitute_food = Food.objects.get(pk=substitute_food)
    substitute_food2 = Food.objects.get(pk=substitute_food2)
    create_substitute_saved = Substitute.objects.create(user=request.user,
                                                        food=substitute_food2, substitut=substitute_food)
    create_substitute_saved.save()
    messages.info(request, 'Votre aliment substitué a été sauvegardé !')
    return redirect('substitute_saved')


@login_required
def substitute_saved(request):
    """return food and substitute saved page"""
    user = Substitute.objects.filter(user=request.user)
    paginator = Paginator(user, 5)
    page = request.GET.get('page')
    paginator_user = paginator.get_page(page)
    return render(request, 'off/substitute_saved.html', {
        'user': paginator_user,
        })


def legal(request):
    return render(request, 'off/legal.html')
