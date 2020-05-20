from django.core.management.base import BaseCommand, CommandError
from off.models import Food
import psycopg2
import requests


class OpenFoodFact:
    '''Class that manages the data retrievement'''
    def __init__(self):
        self.connexion_data_base = psycopg2.connect(database="nutella", user="yohan",
                                                    password="logitech", host="127.0.0.1", port="5432")
        self.data_base = DataBasePsql()
        self.get_food()

    def get_food(self):
        '''Get food from API's openfoodfacts'''
        nb_food = 1000
        parameters = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'sort_by': 'unique_scans_n',
            'page_size': '{}'.format(nb_food),
            'countries': 'France',
            'json': 1,
            'page': 1
        }
        r_food = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=parameters)
        food_json = r_food.json()
        data_food = food_json.get('products')

        for j in range(nb_food):
            food = [d.get('product_name_fr') for d in data_food]
            category = [d.get('categories') for d in data_food]
            ingredients = [d.get('ingredients_text_fr') for d in data_food]
            nutriscore = [d.get('nutriscore_grade') for d in data_food]
            store = [d.get('stores') for d in data_food]
            link = [d.get('url') for d in data_food]
            image_product = [d.get('image_front_url') for d in data_food]
            image_ingredients = [d.get('image_nutrition_url') for d in data_food]
            self.data_base.insert_data_food(food[j], category[j], ingredients[j], nutriscore[j],
                                            store[j], link[j], image_product[j], image_ingredients[j])

        self.data_base.delete_duplicate()
        self.data_base.delete_food_is_null()
        self.data_base.delete_nutriscore_is_null()
        self.data_base.delete_image_product_is_null()
        self.data_base.delete_image_ingredients_is_null()


class DataBasePsql:
    '''Class that manages the creation database and insertion of data'''
    def __init__(self):
        self.connexion_data_base = psycopg2.connect(database="nutella", user="yohan",
                                                    password="logitech", host="127.0.0.1", port="5432")
        self.cursor = self.connexion_data_base.cursor()
        self.connexion_data_base.commit()

    def insert_data_food(self, food, category, ingredients, nutriscore, store, link, image_product, image_ingredients):
        '''Method for insert data food in my database'''
        self.cursor = self.connexion_data_base.cursor()
        add_food = (""" INSERT INTO off_food (food, category, ingredients, nutriscore, store, link, image_product, image_ingredients)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""")
        self.cursor.execute(add_food, (food, category, ingredients, nutriscore, store, link, image_product, image_ingredients, ))
        self.connexion_data_base.commit()
        self.cursor.close()

    def delete_duplicate(self):
        '''delete duplicate food'''
        self.cursor = self.connexion_data_base.cursor()
        delete_duplicate = (""" DELETE FROM off_food a USING off_food b WHERE a.id < b.id AND a.food = b.food; """)
        self.cursor.execute(delete_duplicate)
        self.connexion_data_base.commit()
        self.cursor.close()

    def delete_food_is_null(self):
        self.cursor = self.connexion_data_base.cursor()
        delete_food_is_null = (""" DELETE FROM off_food WHERE food IS NULL; """)
        delete_nutriscore_is_null = (""" DELETE FROM off_food WHERE nutriscore IS NULL; """)
        self.cursor.execute(delete_food_is_null, delete_nutriscore_is_null)
        self.connexion_data_base.commit()
        self.cursor.close()

    def delete_nutriscore_is_null(self):
        self.cursor = self.connexion_data_base.cursor()
        delete_nutriscore_is_null = (""" DELETE FROM off_food WHERE nutriscore IS NULL; """)
        self.cursor.execute(delete_nutriscore_is_null)
        self.connexion_data_base.commit()
        self.cursor.close()

    def delete_image_product_is_null(self):
        self.cursor = self.connexion_data_base.cursor()
        delete_image_product_is_null = (""" DELETE FROM off_food WHERE image_product IS NULL; """)
        delete_image_ingredients_is_null = (""" DELETE FROM off_food WHERE image_ingredients IS NULL; """)
        self.cursor.execute(delete_image_product_is_null)
        self.connexion_data_base.commit()
        self.cursor.close()

    def delete_image_ingredients_is_null(self):
        self.cursor = self.connexion_data_base.cursor()
        delete_image_ingredients_is_null = (""" DELETE FROM off_food WHERE image_ingredients IS NULL; """)
        self.cursor.execute(delete_image_ingredients_is_null)
        self.connexion_data_base.commit()
        self.cursor.close()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading ....'))
        OpenFoodFact().get_food()
