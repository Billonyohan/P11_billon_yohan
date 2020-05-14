from django.contrib import admin
from .models import Food
"""model for django admin"""


class FoodInline(admin.TabularInline):
    model = Food
    extra = 0
    verbose_name = "Aliments"
    verbose_name_plural = "Aliments"


class FoodAdmin(admin.ModelAdmin):
    search_fields = ['food']


admin.site.register(Food, FoodAdmin)
