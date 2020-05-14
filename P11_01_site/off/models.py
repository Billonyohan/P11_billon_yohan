from django.db import models
from django.contrib.auth.models import User
"""model food and substitute"""


class Food(models.Model):
    food = models.TextField(max_length=50)
    category = models.TextField(max_length=300)
    ingredients = models.TextField(max_length=500)
    nutriscore = models.TextField(max_length=50, blank=True, null=True)
    store = models.TextField(max_length=100, null=True)
    link = models.TextField(max_length=100, null=True)
    image_product = models.TextField(max_length=100, null=True)
    image_ingredients = models.TextField(max_length=100, null=True)

    class Meta:
        verbose_name = "Aliments"
        verbose_name_plural = "Aliments"

    def __str__(self):
        return '%s' % (self.food)


class Substitute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='foods')
    substitut = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='substitut')

    class Meta:
        verbose_name = "Substitut utilisateur"
        verbose_name_plural = "Substitut utilisateur"

    def __str__(self):
        return '%s' % (self.user.username)

