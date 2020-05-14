from django.test import TestCase, RequestFactory
from off.models import Food
from django.contrib.auth.models import User
from django.urls import reverse


class IndexTest(TestCase):
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class ViewTest(TestCase):
    def setUp(self):
        Food.objects.create(food="Tomate", category="Fruits", ingredients="Tomate", nutriscore="a",
                            store="leclerc", link="url", image_product="url", image_ingredients="url")
        Food.objects.create(food="Cerise", category="Fruits", ingredients="Tomate", nutriscore="a",
                            store="leclerc", link="url", image_product="url", image_ingredients="url")
        Food.objects.create(food="Orange", category="Fruits", ingredients="Tomate", nutriscore="a",
                            store="leclerc", link="url", image_product="url", image_ingredients="url")
        Food.objects.create(food="Poire", category="Fruits", ingredients="Tomate", nutriscore="a",
                            store="leclerc", link="url", image_product="url", image_ingredients="url")
        self.user = User.objects.create(password="marlc12", username="marc")
        self.factory = RequestFactory()
        self.client.login(username='marc', password='marlc12')

    def test_result_search_views(self):
        """test if result search returns result"""
        food = Food.objects.get(food__contains="Tomate")
        form = {'query': food}
        response = self.client.get(reverse('result_search'), form)
        self.assertEqual(response.status_code, 200)

    def test_result_search_views_no_result(self):
        """test if result search returns 0 result"""
        food = 0
        form = {'query': food}
        response = self.client.get(reverse('result_search'), form)
        self.assertEqual(response.status_code, 200)

    def test_food_details_views(self):
        """test if returns description for food"""
        tomate = Food.objects.get(food__icontains="Tomate")
        form = {'details': tomate}
        response = self.client.get(reverse('description'), form)
        self.assertEqual(response.status_code, 200)

    def test_substitute_views(self):
        """test if substitute returns result"""
        tomate = Food.objects.get(food__contains="Tomate")
        form = {'foods_subtitute': tomate}
        response = self.client.get(reverse('substitute'), form)
        self.assertEqual(response.status_code, 200)

    def test_saved_substitute(self):
        """test if food and subsitute is saved"""
        request = self.factory.get(reverse('saved_substitute'))
        self.client.login(username='marc', password='marlc12')
        request.user = self.user
        tomate = Food.objects.get(food__contains="Tomate")
        poire = Food.objects.get(food__contains="Poire")
        form = {
                'saved_substitute': tomate.id,
                'saved_substitute2': poire.id,
                }
        self.client.force_login(self.user)
        response = self.client.get(reverse('saved_substitute'), form)
        self.assertEqual(response.status_code, 302)

    def test_substitute_saved(self):
        """test if food and subsitute is saved"""
        self.client.login(username='marc', password='marlc12')
        user = User.objects.get(username="marc")
        form = {'paginator_user': user}
        self.client.force_login(self.user)
        response = self.client.get(reverse('substitute_saved'), form)
        self.assertEqual(response.status_code, 200)

    def test_legal(self):
        """test if legal page is returned"""
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)
